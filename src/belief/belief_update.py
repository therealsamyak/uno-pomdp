"""
Belief update operators τ for UNO POMDP.

Follows MATH.md §7: Belief Update
"""

from ..core import Action, Observation
from ..models import Policy
from .particle_filter import ParticleFilter


def update_belief(
    belief: ParticleFilter,
    action: Action,
    observation: Observation,
    opponent_policy: Policy,
) -> None:
    """
    Belief update operator: b_{t+1} = τ(b_t, a_t, o_{t+1})

    Combines:
    1. Prediction step (Chapman-Kolmogorov): b̄_{t+1}(s') = Σ_s P(s'|s,a_t) · b_t(s)
    2. Correction step (Bayes Rule): b_{t+1}(s') = P(o_{t+1}|s') · b̄_{t+1}(s') / Z

    For particle filter, this is:
    1. Prediction: Propagate particles through Player 1's action
    2. Opponent response: Apply opponent policy and transition
    3. Update: Weight by observation likelihood
    4. Resample: If ESS is low

    Args:
        belief: Current belief b_t (modified in place)
        action: Player 1's action a_t
        observation: New observation o_{t+1}
        opponent_policy: Opponent policy π_2
    """
    # Set opponent policy for belief updates
    belief.opponent_policy = opponent_policy

    # 1. Prediction: Apply Player 1's action
    belief.predict(action)

    # 2. Update: Apply opponent response and weight by observation
    belief.update_opponent_response(observation)


def infer_opponent_action(
    observation_before: Observation, observation_after: Observation
) -> str:
    """
    Infer opponent's action from consecutive observations.

    From MATH.md §7.3 and §7.4:
    - If T^{t+1} ≠ T^t AND n_2^{t+1} = n_2^t - 1: Opponent played card
    - If T^{t+1} = T^t AND n_2^{t+1} > n_2^t: Opponent drew cards

    Args:
        observation_before: Observation before opponent's turn o_t
        observation_after: Observation after opponent's turn o_{t+1}

    Returns:
        "play", "draw", or "unknown"
    """
    top_changed = (
        observation_after.top_card.card.id != observation_before.top_card.card.id
        or observation_after.top_card.declared_color
        != observation_before.top_card.declared_color
    )

    hand_size_before = observation_before.opponent_hand_size
    hand_size_after = observation_after.opponent_hand_size

    # Opponent played a card
    if top_changed and hand_size_after == hand_size_before - 1:
        return "play"

    # Opponent drew cards
    if not top_changed and hand_size_after > hand_size_before:
        return "draw"

    return "unknown"
