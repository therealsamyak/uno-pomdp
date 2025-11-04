"""
State space S for 2-player UNO POMDP.

Follows MATH.md §2: State Space
"""

from dataclasses import dataclass
from typing import Optional

from .cards import Card, Color


@dataclass
class TopCard:
    """
    Top card state T^t = (c_top, c̃) ∈ K × C

    - c_top: The card on top of the discard pile
    - declared_color: The active/declared color c̃ ∈ C
      - If c_top is not wild: c̃ = color(c_top)
      - If c_top is wild: c̃ is the color declared when it was played
    """

    card: Card
    declared_color: Color

    def __repr__(self) -> str:
        return f"TopCard({self.card}, declared: {self.declared_color.value})"


@dataclass
class GameState:
    """
    Complete state s_t = (H_1^t, H_2^t, D^t, P^t, T^t, turn^t, meta^t) ∈ S

    Components:
    - hand_1: Player 1's hand (multiset of cards)
    - hand_2: Player 2's hand (multiset of cards)
    - deck: Draw deck D^t (multiset, unordered)
    - discard: Discard pile P^t (multiset, unordered, includes c_top)
    - top_card: Active top card and declared color T^t
    - turn: Active player (1 or 2)
    - draw_penalty: Accumulated draw penalty n_draw ∈ ℕ_0

    State consistency constraint:
    H_1 ∪ H_2 ∪ D ∪ P = K (partition of full deck)
    """

    hand_1: list[Card]
    hand_2: list[Card]
    deck: list[Card]
    discard: list[Card]
    top_card: TopCard
    turn: int  # 1 or 2
    draw_penalty: int  # n_draw

    def __post_init__(self):
        assert self.turn in {1, 2}, f"turn must be 1 or 2, got {self.turn}"
        assert self.draw_penalty >= 0, (
            f"draw_penalty must be non-negative, got {self.draw_penalty}"
        )
        # Note: top_card.card should be in discard, but we don't enforce here for flexibility

    def is_terminal(self) -> bool:
        """
        Check if state is terminal.

        Terminal states: S_term = {s ∈ S : |H_1| = 0 or |H_2| = 0}

        Additional termination: If during a draw action, after reshuffle
        |D^{t+}| < k where k is required draw count, game terminates.
        (This is handled during transitions, not as static state property)
        """
        return len(self.hand_1) == 0 or len(self.hand_2) == 0

    def get_active_hand(self) -> list[Card]:
        """Get the hand of the active player"""
        return self.hand_1 if self.turn == 1 else self.hand_2

    def get_opponent_hand(self) -> list[Card]:
        """Get the hand of the non-active player"""
        return self.hand_2 if self.turn == 1 else self.hand_1

    def copy(self) -> "GameState":
        """Create a deep copy of the state"""
        return GameState(
            hand_1=self.hand_1.copy(),
            hand_2=self.hand_2.copy(),
            deck=self.deck.copy(),
            discard=self.discard.copy(),
            top_card=TopCard(self.top_card.card, self.top_card.declared_color),
            turn=self.turn,
            draw_penalty=self.draw_penalty,
        )
