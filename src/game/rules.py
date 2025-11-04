"""
Game rules for 2-player UNO POMDP.

Follows MATH.md §4: Action Space (playability and legal actions)
"""

from typing import Optional

from ..core import Action, Card, Color, DrawAction, GameState, PlayAction, Rank


def is_playable(card: Card, top_card_info: tuple[Card, Color]) -> bool:
    """
    Check if a card is playable on the current top card.

    Playability function from MATH.md:
    playable(c, T) = {
        true if rank(c) ∈ W (wild cards always playable)
        true if color(c) = c̃ (matches declared color)
        true if rank(c) = rank(c_top) (matches rank)
        false otherwise
    }

    Args:
        card: Card to check
        top_card_info: Tuple of (c_top, declared_color)

    Returns:
        True if card is playable, False otherwise
    """
    c_top, declared_color = top_card_info

    # Wild cards always playable
    if card.rank in {Rank.WILD, Rank.WILD_DRAW_FOUR}:
        return True

    # Match declared color
    if card.color == declared_color:
        return True

    # Match rank
    if card.rank == c_top.rank:
        return True

    return False


def get_playable_cards(
    hand: list[Card], top_card_info: tuple[Card, Color]
) -> list[Card]:
    """
    Get all playable cards from a hand.

    Args:
        hand: Player's hand
        top_card_info: Tuple of (c_top, declared_color)

    Returns:
        List of playable cards
    """
    return [card for card in hand if is_playable(card, top_card_info)]


def get_playable_actions(state: GameState) -> list[PlayAction]:
    """
    Get all playable card actions for the active player.

    A_playable(s_t) = {(c, c̃) : c ∈ H_i^t, playable(c, T^t),
                       c̃ = color(c) if rank(c) ∉ W,
                       c̃ ∈ C if rank(c) ∈ W}

    Args:
        state: Current game state

    Returns:
        List of all playable actions
    """
    active_hand = state.get_active_hand()
    top_card_info = (state.top_card.card, state.top_card.declared_color)

    playable_actions: list[PlayAction] = []

    for card in active_hand:
        if is_playable(card, top_card_info):
            if card.is_wild():
                # Wild cards can be played with any color declaration
                for color in Color:
                    playable_actions.append(PlayAction(card, color))
            else:
                # Non-wild cards must declare their inherent color
                playable_actions.append(PlayAction(card, card.color))

    return playable_actions


def get_legal_actions(state: GameState) -> list[Action]:
    """
    Get all legal actions for the active player in the current state.

    Legal action set from MATH.md:
    A_legal(s_t) = {
        {Draw} if n_draw > 0 (penalty active, must draw)
        A_playable(s_t) if n_draw = 0 and A_playable ≠ ∅ (can only play if playable cards exist)
        {Draw} if n_draw = 0 and A_playable = ∅ (no playable cards, must draw)
    }

    Rule: You can only draw if you have no playable cards (or if a draw penalty is active).

    2-Player Special Rules:
    - Reverse acts as Skip (ends turn immediately)
    - No stacking of draw penalties (cannot play +2 or Wild+4 when n_draw > 0)
    - No challenging Wild+4

    Args:
        state: Current game state

    Returns:
        List of legal actions
    """
    # If penalty is active, must draw
    if state.draw_penalty > 0:
        return [DrawAction()]

    # Get playable card actions
    playable_actions = get_playable_actions(state)

    # If playable cards exist, can only play (not draw)
    if playable_actions:
        return playable_actions

    # No playable cards, must draw
    return [DrawAction()]


def can_play_card(state: GameState, card: Card) -> bool:
    """
    Check if a specific card can be played in the current state.

    Args:
        state: Current game state
        card: Card to check

    Returns:
        True if card is in active player's hand and playable
    """
    active_hand = state.get_active_hand()
    if card not in active_hand:
        return False

    top_card_info = (state.top_card.card, state.top_card.declared_color)
    return is_playable(card, top_card_info)
