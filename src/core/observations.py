"""
Observation space Ω for Player 1 in 2-player UNO POMDP.

Follows MATH.md §3: Observation Space
"""

from dataclasses import dataclass

from .cards import Card
from .state import TopCard


@dataclass
class Observation:
    """
    Player 1's observation at time t:
    o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, meta_obs^t) ∈ Ω

    Components:
    - hand_1: Player 1's hand (fully observed)
    - opponent_hand_size: n_2^t = |H_2^t| (opponent's hand size)
    - deck_size: n_d^t = |D^t| (draw deck size)
    - discard: P^t (discard pile multiset, visible)
    - top_card: T^t (top card and declared color, visible)
    - draw_penalty: n_draw (observable metadata)

    Observation likelihood:
    P(o_t | s_t) = 𝟙[proj(s_t) = o_t]

    This filters out impossible states from possible states.
    """

    hand_1: list[Card]
    opponent_hand_size: int
    deck_size: int
    discard: list[Card]
    top_card: TopCard
    draw_penalty: int

    def __post_init__(self):
        assert self.opponent_hand_size >= 0, "opponent_hand_size must be non-negative"
        assert self.deck_size >= 0, "deck_size must be non-negative"
        assert self.draw_penalty >= 0, "draw_penalty must be non-negative"

    def __repr__(self) -> str:
        return (
            f"Observation(\n"
            f"  hand_1: {len(self.hand_1)} cards,\n"
            f"  opponent_hand_size: {self.opponent_hand_size},\n"
            f"  deck_size: {self.deck_size},\n"
            f"  discard: {len(self.discard)} cards,\n"
            f"  top_card: {self.top_card},\n"
            f"  draw_penalty: {self.draw_penalty}\n"
            f")"
        )
