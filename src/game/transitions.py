"""
State transition dynamics T for 2-player UNO POMDP.

Follows MATH.md §5: State Transition Dynamics
"""

import random
from typing import Optional

from ..core import Action, DrawAction, GameState, PlayAction, Rank, TopCard


class InsufficientCardsError(Exception):
    """Raised when not enough cards to draw after reshuffle"""

    pass


def draw_cards_from_deck(deck: list, k: int) -> tuple[list, list]:
    """
    Draw k cards uniformly at random from an unordered deck (multiset).

    Since D^t is unordered, sample k cards uniformly at random without replacement.
    Each k-subset has equal probability 1/C(|D|, k).

    Args:
        deck: Current deck (will be modified)
        k: Number of cards to draw

    Returns:
        Tuple of (drawn_cards, remaining_deck)

    Raises:
        ValueError: If deck has fewer than k cards
    """
    if len(deck) < k:
        raise ValueError(f"Cannot draw {k} cards from deck of size {len(deck)}")

    # Sample k cards uniformly at random
    drawn_cards = random.sample(deck, k)

    # Remove drawn cards from deck
    remaining_deck = deck.copy()
    for card in drawn_cards:
        remaining_deck.remove(card)

    return drawn_cards, remaining_deck


def reshuffle_deck(deck: list, discard: list, top_card) -> tuple[list, list]:
    """
    Reshuffle: combine discard (except top card) with deck.

    From MATH.md:
    D^{t+} = (P^t \ {c_top}) ∪ D^t
    P^{t+} = {c_top}

    Args:
        deck: Current deck
        discard: Current discard pile (includes top card)
        top_card: Top card to keep in discard

    Returns:
        Tuple of (new_deck, new_discard)
    """
    # Combine deck with all discard cards except top card
    new_deck = deck.copy()
    for card in discard:
        if card.id != top_card.id:
            new_deck.append(card)

    # New discard pile contains only top card
    new_discard = [top_card]

    return new_deck, new_discard


def apply_draw_action(state: GameState) -> GameState:
    """
    Apply a draw action to the state.

    From MATH.md §5.1 (Drawing):
    1. Determine draw count: k = max(1, n_draw)
    2. If |D^t| < k: Reshuffle
       - If |D^{t+}| < k after reshuffle: Game ends (terminal)
    3. Sample k cards uniformly from D^{t+}
    4. Update: H_i^{t+} = H_i^t ∪ {d_1, ..., d_k}, D^{t+} = D^{t+} \ {d_1, ..., d_k}
    5. Reset penalty: n_draw^{t+} = 0
    6. Forced end turn: turn^{t+} = opponent

    Args:
        state: Current game state

    Returns:
        New state after drawing

    Raises:
        InsufficientCardsError: If unable to draw k cards after reshuffle
    """
    new_state = state.copy()

    # 1. Determine draw count
    k = max(1, state.draw_penalty)

    # 2. Check if reshuffle needed
    if len(new_state.deck) < k:
        new_deck, new_discard = reshuffle_deck(
            new_state.deck, new_state.discard, new_state.top_card.card
        )
        new_state.deck = new_deck
        new_state.discard = new_discard

        # Check if still insufficient
        if len(new_state.deck) < k:
            raise InsufficientCardsError(
                f"Cannot draw {k} cards: only {len(new_state.deck)} available after reshuffle"
            )

    # 3. Sample k cards uniformly
    drawn_cards, remaining_deck = draw_cards_from_deck(new_state.deck, k)
    new_state.deck = remaining_deck

    # 4. Update active player's hand
    if new_state.turn == 1:
        new_state.hand_1.extend(drawn_cards)
    else:
        new_state.hand_2.extend(drawn_cards)

    # 5. Reset penalty
    new_state.draw_penalty = 0

    # 6. End turn
    new_state.turn = 3 - new_state.turn  # Switch 1→2 or 2→1

    return new_state


def apply_play_action(state: GameState, action: PlayAction) -> GameState:
    """
    Apply a play action to the state.

    From MATH.md §5.1 (Playing a card):
    1. Remove from hand: H_i^{t+} = H_i^t \ {c}
    2. Update top card: T^{t+} = (c, c̃)
    3. Add to discard: P^{t+} = P^t ∪ {c}
    4. Handle card effects:
       - +2: n_draw^{t+} = n_draw^t + 2, turn^{t+} = opponent
       - Wild+4: n_draw^{t+} = n_draw^t + 4, turn^{t+} = opponent
       - Skip or Reverse: turn^{t+} = opponent (acts as Skip in 2-player)
       - Number or Wild: turn^{t+} = opponent

    Args:
        state: Current game state
        action: Play action to apply

    Returns:
        New state after playing card
    """
    new_state = state.copy()
    card = action.card

    # 1. Remove from active player's hand
    if new_state.turn == 1:
        if card not in new_state.hand_1:
            raise ValueError(f"Card {card} not in Player 1's hand")
        new_state.hand_1.remove(card)
    else:
        if card not in new_state.hand_2:
            raise ValueError(f"Card {card} not in Player 2's hand")
        new_state.hand_2.remove(card)

    # 2. Update top card with declared color
    new_state.top_card = TopCard(card, action.declared_color)

    # 3. Add to discard pile
    new_state.discard.append(card)

    # 4. Handle card effects
    if card.rank == Rank.DRAW_TWO:
        new_state.draw_penalty += 2
    elif card.rank == Rank.WILD_DRAW_FOUR:
        new_state.draw_penalty += 4
    # Skip and Reverse both act as Skip in 2-player (end turn immediately)
    # Number cards and Wild cards just end turn normally

    # All cards end the current player's turn
    new_state.turn = 3 - new_state.turn  # Switch 1→2 or 2→1

    return new_state


def apply_action(state: GameState, action: Action) -> GameState:
    """
    Apply an action to the state and return the new state.

    Args:
        state: Current game state
        action: Action to apply

    Returns:
        New state after action

    Raises:
        InsufficientCardsError: If unable to complete draw action
    """
    if isinstance(action, DrawAction):
        return apply_draw_action(state)
    elif isinstance(action, PlayAction):
        return apply_play_action(state, action)
    else:
        raise ValueError(f"Unknown action type: {type(action)}")
