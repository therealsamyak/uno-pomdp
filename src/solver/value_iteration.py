"""
Value iteration solver for UNO POMDP.

Follows MATH.md §10: Value Function and Bellman Optimality
"""

from typing import Callable, Optional

from ..belief import ParticleFilter, update_belief
from ..core import Action, Observation
from ..game import get_legal_actions
from ..models import Policy
from .heuristics import heuristic_q_value


class ValueIterationSolver:
    """
    Value iteration solver for belief-space POMDP.

    From MATH.md:
    V*(b) = max_{a ∈ A} Q*(b, a)
    Q*(b, a) = R(b, a) + γ Σ_{o ∈ Ω} P(o | b, a) · V*(τ(b, a, o))

    For UNO, exact value iteration is intractable, so we use:
    1. Heuristic value approximation
    2. Monte Carlo rollouts for action evaluation
    3. Depth-limited search
    """

    def __init__(
        self,
        discount: float = 0.95,
        max_depth: int = 3,
        num_rollouts: int = 10,
        opponent_policy: Optional[Policy] = None,
    ):
        """
        Args:
            discount: Discount factor γ
            max_depth: Maximum depth for rollout search
            num_rollouts: Number of Monte Carlo rollouts per action
            opponent_policy: Opponent policy π_2
        """
        self.discount = discount
        self.max_depth = max_depth
        self.num_rollouts = num_rollouts
        self.opponent_policy = opponent_policy

    def select_action(
        self, belief: ParticleFilter, actual_state: Optional["GameState"] = None
    ) -> Action:
        """
        Select optimal action: π*(b) = argmax_{a ∈ A} Q*(b, a)

        Args:
            belief: Current belief state
            actual_state: Actual game state (for correct P1 hand). If None, use belief.

        Returns:
            Best action according to value function
        """
        # Use actual state if provided (has correct P1 hand), otherwise use belief
        state = (
            actual_state if actual_state is not None else belief.get_expected_state()
        )
        legal_actions = get_legal_actions(state)

        if not legal_actions:
            raise ValueError("No legal actions available")

        if len(legal_actions) == 1:
            return legal_actions[0]

        # Evaluate each action
        best_action = None
        best_value = float("-inf")

        for action in legal_actions:
            # Use heuristic Q-value
            q_value = heuristic_q_value(belief, action, self.discount)

            if q_value > best_value:
                best_value = q_value
                best_action = action

        return best_action if best_action is not None else legal_actions[0]

    def evaluate_action(
        self, belief: ParticleFilter, action: Action, depth: int = 0
    ) -> float:
        """
        Evaluate action using Monte Carlo rollouts.

        Q(b, a) ≈ (1/K) Σ_{k=1}^K [R(s_k, a) + γ · rollout(s'_k)]

        where s_k ~ b and s'_k ~ P(·|s_k, a)

        Args:
            belief: Current belief
            action: Action to evaluate
            depth: Current search depth

        Returns:
            Estimated Q-value
        """
        from ..game import apply_action, compute_reward

        if depth >= self.max_depth:
            # Use heuristic at depth limit
            return heuristic_q_value(belief, action, self.discount)

        total_value = 0.0

        for _ in range(self.num_rollouts):
            # Sample a state from belief
            state = belief.sample_state()

            try:
                # Apply action
                next_state = apply_action(state, action)

                # Immediate reward
                reward = compute_reward(state, action, next_state)

                # If terminal, done
                if next_state.is_terminal():
                    total_value += reward
                    continue

                # Otherwise, estimate future value
                # For simplicity, use heuristic (full rollout would be too expensive)
                from .heuristics import heuristic_value

                # Create temporary belief for next state
                future_value = 0.0  # Simplified

                total_value += reward + self.discount * future_value

            except Exception:
                # Action failed, penalty
                total_value += -10.0

        return total_value / self.num_rollouts


class OnlinePOMDPPlanner:
    """
    Online POMDP planner that maintains belief and selects actions.

    This is the main interface for using the solver.
    """

    def __init__(
        self,
        solver: ValueIterationSolver,
        opponent_policy: Policy,
        num_particles: int = 1000,
    ):
        """
        Args:
            solver: Value iteration solver
            opponent_policy: Opponent policy π_2
            num_particles: Number of particles for belief tracking
        """
        self.solver = solver
        self.opponent_policy = opponent_policy
        self.num_particles = num_particles
        self.belief: Optional[ParticleFilter] = None

    def initialize(self, observation: Observation, all_cards) -> None:
        """
        Initialize belief from initial observation.

        Args:
            observation: Initial observation o_0
            all_cards: Full deck K
        """
        self.belief = ParticleFilter(
            num_particles=self.num_particles, opponent_policy=self.opponent_policy
        )
        self.belief.initialize_uniform(observation, all_cards)

    def select_action(self, actual_state: Optional["GameState"] = None) -> Action:
        """
        Select best action for current belief.

        Args:
            actual_state: Actual game state (for correct P1 hand)

        Returns:
            Optimal action π*(b)
        """
        if self.belief is None:
            raise ValueError("Belief not initialized")

        return self.solver.select_action(self.belief, actual_state)

    def update(self, action: Action, observation: Observation) -> None:
        """
        Update belief after taking action and receiving observation.

        b_{t+1} = τ(b_t, a_t, o_{t+1})

        Args:
            action: Action taken
            observation: New observation
        """
        if self.belief is None:
            raise ValueError("Belief not initialized")

        update_belief(self.belief, action, observation, self.opponent_policy)
