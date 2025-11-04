"""
UNO POMDP Solver

A complete implementation of 2-player UNO as a Partially Observable Markov Decision Process (POMDP)
with particle filter belief tracking and value iteration solver.

Following the mathematical specification in MATH.md.
"""

from .belief import (
    ParticleFilter,
    compute_unseen_pool,
    expected_playable_cards_in_opponent_hand,
    infer_opponent_action,
    probability_card_in_opponent_hand,
    probability_color_in_opponent_hand,
    update_belief,
)
from .core import (
    Action,
    Card,
    Color,
    DrawAction,
    GameState,
    Observation,
    PlayAction,
    Rank,
    TopCard,
    create_play_action,
    generate_deck,
)
from .game import (
    InsufficientCardsError,
    apply_action,
    can_play_card,
    compute_reward,
    get_legal_actions,
    get_playable_actions,
    is_playable,
)
from .models import GreedyPolicy, HeuristicPolicy, Policy, UniformRandomPolicy
from .pomdp import UNOPOMDP
from .solver import (
    OnlinePOMDPPlanner,
    ValueIterationSolver,
    heuristic_q_value,
    heuristic_value,
)

__version__ = "0.1.0"

__all__ = [
    # Core primitives
    "Card",
    "Color",
    "Rank",
    "GameState",
    "TopCard",
    "Observation",
    "Action",
    "PlayAction",
    "DrawAction",
    "create_play_action",
    "generate_deck",
    # Game logic
    "is_playable",
    "get_playable_actions",
    "get_legal_actions",
    "can_play_card",
    "apply_action",
    "compute_reward",
    "InsufficientCardsError",
    # Policies
    "Policy",
    "UniformRandomPolicy",
    "GreedyPolicy",
    "HeuristicPolicy",
    # Belief tracking
    "ParticleFilter",
    "update_belief",
    "infer_opponent_action",
    "compute_unseen_pool",
    "probability_card_in_opponent_hand",
    "probability_color_in_opponent_hand",
    "expected_playable_cards_in_opponent_hand",
    # Solver
    "ValueIterationSolver",
    "OnlinePOMDPPlanner",
    "heuristic_value",
    "heuristic_q_value",
    # Main POMDP
    "UNOPOMDP",
]
