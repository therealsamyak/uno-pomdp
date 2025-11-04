"""
Game logic for UNO POMDP.
"""

from .rewards import (
    compute_reward,
    compute_reward_with_step_penalty,
    compute_terminal_reward_by_card_count,
)
from .rules import can_play_card, get_legal_actions, get_playable_actions, is_playable
from .transitions import (
    InsufficientCardsError,
    apply_action,
    apply_draw_action,
    apply_play_action,
)

__all__ = [
    # Rules
    "is_playable",
    "get_playable_actions",
    "get_legal_actions",
    "can_play_card",
    # Transitions
    "apply_action",
    "apply_draw_action",
    "apply_play_action",
    "InsufficientCardsError",
    # Rewards
    "compute_reward",
    "compute_reward_with_step_penalty",
    "compute_terminal_reward_by_card_count",
]
