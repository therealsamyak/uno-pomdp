"""
Heuristic value approximations for UNO POMDP.

Follows MATH.md §13: Heuristic Value Approximations
"""

from ..belief import ParticleFilter, expected_playable_cards_in_opponent_hand
from ..core import Card, Rank


def hand_size_difference(belief: ParticleFilter) -> float:
    """
    Hand size difference: n_2 - |H_1|

    Positive when opponent has more cards (good for us).

    Args:
        belief: Current belief state

    Returns:
        Expected hand size difference
    """
    if not belief.particles:
        return 0.0

    expected_diff = 0.0
    for particle in belief.particles:
        diff = len(particle.state.hand_2) - len(particle.state.hand_1)
        expected_diff += particle.weight * diff

    return expected_diff


def expected_opponent_playable_cards(belief: ParticleFilter) -> float:
    """
    Expected number of playable cards in opponent's hand.

    Lower is better (opponent has fewer options).

    Args:
        belief: Current belief state

    Returns:
        Expected number of playable cards opponent holds
    """
    from ..belief import compute_unseen_pool

    if not belief.particles:
        return 0.0

    # Get a representative state for top card
    if not belief.particles:
        return 0.0
    state = belief.get_expected_state()

    # Compute from unseen pool
    from ..core import generate_deck

    all_cards = generate_deck()
    unseen_pool = compute_unseen_pool(state.hand_1, state.discard, all_cards)

    return expected_playable_cards_in_opponent_hand(
        unseen_pool, len(state.hand_2), state.top_card
    )


def count_wild_cards(hand: list[Card]) -> int:
    """
    Count wild cards in hand.

    Wild cards are valuable for flexibility.

    Args:
        hand: Player's hand

    Returns:
        Number of wild cards
    """
    return sum(1 for card in hand if card.rank in {Rank.WILD, Rank.WILD_DRAW_FOUR})


def count_action_cards(hand: list[Card]) -> int:
    """
    Count action cards in hand (+2, Wild+4, Skip, Reverse).

    Action cards are valuable for disrupting opponent.

    Args:
        hand: Player's hand

    Returns:
        Number of action cards
    """
    action_ranks = {Rank.DRAW_TWO, Rank.WILD_DRAW_FOUR, Rank.SKIP, Rank.REVERSE}
    return sum(1 for card in hand if card.rank in action_ranks)


def color_diversity(hand: list[Card]) -> float:
    """
    Measure color diversity in hand.

    Higher diversity = more options.

    Args:
        hand: Player's hand

    Returns:
        Number of different colors in hand (0-4)
    """
    colors = {card.color for card in hand if card.color is not None}
    return len(colors)


def heuristic_value(belief: ParticleFilter) -> float:
    """
    Heuristic value approximation for belief state.

    From MATH.md:
    V_heur(b) = α_1 · (n_2 - |H_1|) + α_2 · f_playable(b) + α_3 · f_wild(H_1)

    We extend this with more features for better play.

    Args:
        belief: Current belief state

    Returns:
        Heuristic value estimate (positive = good for Player 1)
    """
    if not belief.particles:
        return 0.0

    # Get representative state
    state = belief.get_expected_state()

    # Check terminal conditions
    if len(state.hand_1) == 0:
        return 100.0  # Player 1 wins
    if len(state.hand_2) == 0:
        return -100.0  # Player 2 wins

    # Feature weights (tuned for balance)
    α_hand_diff = 2.0
    α_opponent_playable = -1.5
    α_wild = 3.0
    α_action = 2.0
    α_color_diversity = 1.0

    # Compute features
    hand_diff = hand_size_difference(belief)
    opp_playable = expected_opponent_playable_cards(belief)
    wilds = count_wild_cards(state.hand_1)
    actions = count_action_cards(state.hand_1)
    colors = color_diversity(state.hand_1)

    # Combine weighted features
    value = (
        α_hand_diff * hand_diff
        + α_opponent_playable * opp_playable
        + α_wild * wilds
        + α_action * actions
        + α_color_diversity * colors
    )

    return value


def heuristic_q_value(belief: ParticleFilter, action, discount: float = 0.95) -> float:
    """
    Heuristic Q-value for action in belief state.

    Q_heur(b, a) ≈ R(b, a) + γ · V_heur(b')

    where b' is the belief after taking action a (approximately).

    This is a rough approximation without full belief propagation.

    Args:
        belief: Current belief state
        action: Action to evaluate
        discount: Discount factor γ

    Returns:
        Heuristic Q-value estimate
    """
    from ..game import apply_action, compute_reward

    # Get representative state
    state = belief.get_expected_state()

    # Simulate action (approximate)
    try:
        next_state = apply_action(state, action)

        # Immediate reward
        reward = compute_reward(state, action, next_state)

        # If terminal, return immediate reward
        if next_state.is_terminal():
            return reward

        # Otherwise, estimate future value
        # For simplicity, just use current belief (not propagated)
        future_value = heuristic_value(belief)

        return reward + discount * future_value

    except Exception:
        # Action failed, return very negative value
        return -1000.0
