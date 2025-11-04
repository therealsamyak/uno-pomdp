"""
Reward function R for 2-player UNO POMDP.

Follows MATH.md §9: Reward Function
"""

from ..core import Action, GameState


def compute_reward(state: GameState, action: Action, next_state: GameState) -> float:
    """
    Compute reward for Player 1 after taking action a in state s, resulting in state s'.

    From MATH.md:
    R(s', a) = {
        +1 if |H_1| = 0 in state s' (Player 1 wins)
        -1 if |H_2| = 0 in state s' (Player 2 wins)
        +1 if game ends due to inability to draw and |H_1| < |H_2| (Player 1 wins by fewer cards)
        -1 if game ends due to inability to draw and |H_2| < |H_1| (Player 2 wins by fewer cards)
        0 if game ends due to inability to draw and |H_1| = |H_2| (draw)
        0 otherwise
    }

    Args:
        state: Original state
        action: Action taken
        next_state: Resulting state

    Returns:
        Reward for Player 1 (from perspective of Player 1)
    """
    # Check for normal win condition
    if len(next_state.hand_1) == 0:
        return 1.0  # Player 1 wins

    if len(next_state.hand_2) == 0:
        return -1.0  # Player 2 wins

    # Non-terminal state
    return 0.0


def compute_terminal_reward_by_card_count(hand_1_size: int, hand_2_size: int) -> float:
    """
    Compute reward when game ends due to insufficient cards (after reshuffle).

    Args:
        hand_1_size: Size of Player 1's hand
        hand_2_size: Size of Player 2's hand

    Returns:
        +1 if Player 1 has fewer cards (wins)
        -1 if Player 2 has fewer cards (wins)
        0 if tied (draw)
    """
    if hand_1_size < hand_2_size:
        return 1.0  # Player 1 wins
    elif hand_2_size < hand_1_size:
        return -1.0  # Player 2 wins
    else:
        return 0.0  # Draw


def compute_reward_with_step_penalty(
    state: GameState, action: Action, next_state: GameState, step_penalty: float = 0.01
) -> float:
    """
    Compute reward with per-step penalty to encourage shorter games.

    R(s, a) = R_terminal(s') - λ · 𝟙[s' ∉ S_term]

    Args:
        state: Original state
        action: Action taken
        next_state: Resulting state
        step_penalty: Penalty λ for non-terminal states

    Returns:
        Reward for Player 1 with step penalty
    """
    base_reward = compute_reward(state, action, next_state)

    # Apply step penalty if not terminal
    if not next_state.is_terminal():
        base_reward -= step_penalty

    return base_reward
