"""
Tractable marginal computations for belief state.

Follows MATH.md §12: Tractable Marginal Computations
"""

from typing import Callable

from ..core import Card, Color, GameState, TopCard
from ..game import is_playable


def compute_unseen_pool(
    hand_1: list[Card], discard: list[Card], all_cards: list[Card]
) -> list[Card]:
    """
    Compute unseen pool: U_t = K \ (H_1^t ∪ P^t)

    Cards not in Player 1's hand or discard pile.

    Args:
        hand_1: Player 1's hand
        discard: Discard pile
        all_cards: Full deck K

    Returns:
        List of unseen cards
    """
    # Get IDs of known cards
    known_ids = {card.id for card in hand_1} | {card.id for card in discard}

    # Return cards not in known set
    return [card for card in all_cards if card.id not in known_ids]


def probability_card_in_opponent_hand(
    card: Card, unseen_pool: list[Card], opponent_hand_size: int
) -> float:
    """
    Probability that a specific card is in opponent's hand under uniform belief.

    P(c ∈ H_2) = n_2 / m_t

    where n_2 = |H_2| and m_t = |U_t|

    Args:
        card: Card to check
        unseen_pool: Unseen pool U_t
        opponent_hand_size: Size of opponent's hand n_2

    Returns:
        Probability that card is in opponent's hand
    """
    if card not in unseen_pool:
        return 0.0

    m_t = len(unseen_pool)
    if m_t == 0:
        return 0.0

    return opponent_hand_size / m_t


def probability_color_in_opponent_hand(
    color: Color, unseen_pool: list[Card], opponent_hand_size: int
) -> float:
    """
    Probability that opponent has at least one card of given color.

    P(∃k ∈ H_2 : color(k) = c) = 1 - C(m_t - m_c, n_2) / C(m_t, n_2)

    where m_c = |{k ∈ U_t : color(k) = c}|

    Args:
        color: Color to check
        unseen_pool: Unseen pool U_t
        opponent_hand_size: Size of opponent's hand n_2

    Returns:
        Probability opponent has at least one card of the color
    """
    from math import comb

    m_t = len(unseen_pool)
    n_2 = opponent_hand_size

    if m_t == 0 or n_2 == 0:
        return 0.0

    # Count cards of given color in unseen pool
    m_c = sum(1 for card in unseen_pool if card.color == color)

    if m_c == 0:
        return 0.0

    if n_2 > m_t:
        return 0.0  # Invalid: hand size exceeds unseen pool

    if n_2 > m_t - m_c:
        return 1.0  # Must have at least one of the color

    # Probability of NOT having the color
    prob_none = comb(m_t - m_c, n_2) / comb(m_t, n_2)

    return 1.0 - prob_none


def expected_playable_cards_in_opponent_hand(
    unseen_pool: list[Card], opponent_hand_size: int, top_card: TopCard
) -> float:
    """
    Expected number of playable cards opponent holds.

    E[|{k ∈ H_2 : playable(k, T^t)}|] = Σ_{k ∈ U_t} 𝟙[playable(k, T^t)] · (n_2 / m_t)

    Args:
        unseen_pool: Unseen pool U_t
        opponent_hand_size: Size of opponent's hand n_2
        top_card: Current top card T^t

    Returns:
        Expected number of playable cards in opponent's hand
    """
    m_t = len(unseen_pool)
    n_2 = opponent_hand_size

    if m_t == 0:
        return 0.0

    top_card_info = (top_card.card, top_card.declared_color)

    # Count playable cards in unseen pool
    playable_count = sum(1 for card in unseen_pool if is_playable(card, top_card_info))

    # Expected value under uniform distribution
    return playable_count * (n_2 / m_t)


def sample_opponent_hand_uniform(
    unseen_pool: list[Card], opponent_hand_size: int
) -> list[Card]:
    """
    Sample opponent's hand uniformly from unseen pool.

    Used for particle filter initialization.

    Args:
        unseen_pool: Unseen pool U_t
        opponent_hand_size: Size of opponent's hand n_2

    Returns:
        Sampled opponent hand (random subset of unseen pool)
    """
    import random

    if opponent_hand_size > len(unseen_pool):
        raise ValueError(
            f"Cannot sample hand of size {opponent_hand_size} "
            f"from unseen pool of size {len(unseen_pool)}"
        )

    return random.sample(unseen_pool, opponent_hand_size)
