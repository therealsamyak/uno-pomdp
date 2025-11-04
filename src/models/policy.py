"""
Policy π for 2-player UNO POMDP.

Follows MATH.md §5.2: Opponent Model

Both players use the same policy to check for Nash equilibrium.
"""

import random
from typing import Protocol

from ..core import Action, DrawAction, GameState, PlayAction
from ..game import get_legal_actions, get_playable_actions


class Policy(Protocol):
    """Protocol for a policy π(a | s)"""

    def select_action(self, state: GameState) -> Action:
        """Select an action given the state"""
        ...

    def get_action_probability(self, state: GameState, action: Action) -> float:
        """Get probability of selecting action in state"""
        ...


class UniformRandomPolicy:
    """
    Uniform random policy: π^unif(a | s) = 𝟙[a ∈ A_legal(s)] / |A_legal(s)|

    Uniformly randomizes over all legal actions.
    """

    def select_action(self, state: GameState) -> Action:
        """Select action uniformly at random from legal actions"""
        legal_actions = get_legal_actions(state)
        if not legal_actions:
            raise ValueError("No legal actions available")
        return random.choice(legal_actions)

    def get_action_probability(self, state: GameState, action: Action) -> float:
        """Get probability of selecting action (uniform over legal actions)"""
        legal_actions = get_legal_actions(state)
        if action in legal_actions:
            return 1.0 / len(legal_actions)
        return 0.0


class GreedyPolicy:
    """
    Greedy policy: prefers playing cards over drawing.

    π^greedy(a | s) = {
        𝟙[a ∈ A_playable(s)] / |A_playable(s)| if A_playable(s) ≠ ∅
        1 if a = Draw and A_playable(s) = ∅
    }

    This policy uniformly randomizes over playable cards when available,
    otherwise draws.
    """

    def select_action(self, state: GameState) -> Action:
        """Select action, preferring plays over draws"""
        playable_actions = get_playable_actions(state)

        # If we have playable cards and no penalty, play one
        if playable_actions and state.draw_penalty == 0:
            return random.choice(playable_actions)

        # Otherwise, must draw (either penalty active or no playable cards)
        return DrawAction()

    def get_action_probability(self, state: GameState, action: Action) -> float:
        """Get probability of selecting action"""
        playable_actions = get_playable_actions(state)

        # If penalty active, must draw
        if state.draw_penalty > 0:
            return 1.0 if isinstance(action, DrawAction) else 0.0

        # If playable cards exist, uniform over them
        if playable_actions:
            if action in playable_actions:
                return 1.0 / len(playable_actions)
            return 0.0

        # No playable cards, must draw
        return 1.0 if isinstance(action, DrawAction) else 0.0


class HeuristicPolicy:
    """
    Heuristic-based policy for better play.

    Priorities:
    1. If can win (play last card), do so
    2. Prefer action cards (+2, Wild+4, Skip, Reverse) to hinder opponent
    3. Prefer playing cards that reduce hand size
    4. Prefer matching color over matching rank (more future playability)
    5. Save wild cards for when needed
    """

    def __init__(self, randomness: float = 0.1):
        """
        Args:
            randomness: Probability of taking random action instead of heuristic
        """
        self.randomness = randomness

    def select_action(self, state: GameState) -> Action:
        """Select action using heuristics"""
        # Get legal actions (respects draw penalty and playability)
        legal_actions = get_legal_actions(state)

        if not legal_actions:
            raise ValueError("No legal actions available")

        # Sometimes act randomly for exploration
        if random.random() < self.randomness:
            return random.choice(legal_actions)

        # If only one legal action, must take it
        if len(legal_actions) == 1:
            return legal_actions[0]

        # If forced to draw (penalty active or no playable cards)
        if isinstance(legal_actions[0], DrawAction):
            return legal_actions[0]

        # Otherwise, score play actions and pick best
        active_hand = state.get_active_hand()

        # If can win (playing last card), do so immediately
        if len(active_hand) == 1:
            return legal_actions[0]

        # Score each action and pick best
        best_action = None
        best_score = float("-inf")

        for action in legal_actions:
            if isinstance(action, DrawAction):
                continue  # Shouldn't happen here but skip if present
            score = self._score_action(action, state)
            if score > best_score:
                best_score = score
                best_action = action

        return best_action if best_action is not None else legal_actions[0]

    def _score_action(self, action: PlayAction, state: GameState) -> float:
        """Score an action based on heuristics"""
        from ..core import Rank

        score = 0.0
        card = action.card

        # Prefer action cards
        if card.rank == Rank.WILD_DRAW_FOUR:
            score += 10.0
        elif card.rank == Rank.DRAW_TWO:
            score += 8.0
        elif card.rank in {Rank.SKIP, Rank.REVERSE}:
            score += 6.0

        # Prefer matching color over rank (maintains color control)
        if not card.is_wild():
            if card.color == state.top_card.declared_color:
                score += 3.0

        # Slightly prefer non-wild over wild (save wilds for emergencies)
        if card.rank == Rank.WILD or card.rank == Rank.WILD_DRAW_FOUR:
            score -= 2.0

        # Prefer cards we have duplicates of (less hand diversity loss)
        active_hand = state.get_active_hand()
        duplicate_count = sum(1 for c in active_hand if c.rank == card.rank)
        score += duplicate_count * 0.5

        return score

    def get_action_probability(self, state: GameState, action: Action) -> float:
        """
        Get approximate probability of selecting action.

        Note: This is approximate since we have randomness and tie-breaking.
        """
        playable_actions = get_playable_actions(state)
        legal_actions = get_legal_actions(state)

        # Random component
        uniform_prob = (1.0 / len(legal_actions)) * self.randomness

        # Heuristic component (deterministic best action)
        if action == self.select_action(state):
            return uniform_prob + (1.0 - self.randomness)

        return uniform_prob
