"""
Particle filter for belief state tracking in UNO POMDP.

Follows MATH.md §11.2: Particle Filter (Approximate)
"""

import random
from dataclasses import dataclass
from typing import Optional

from ..core import Action, Card, GameState, Observation
from ..game import apply_action
from ..models import Policy


@dataclass
class Particle:
    """
    A weighted particle representing a possible complete state.

    Particle filter approximates belief:
    b_t ≈ {(s^(i), w^(i))}_{i=1}^N, Σ w^(i) = 1
    """

    state: GameState
    weight: float


class ParticleFilter:
    """
    Particle filter for belief state tracking.

    Algorithm (from MATH.md):
    1. Prediction: For each particle s^(i), sample successor s'^(i) ~ P(· | s^(i), a_t)
    2. Update: Weight by observation likelihood: w'^(i) = w^(i) · P(o_{t+1} | s'^(i))
    3. Normalize: w̃^(i) = w'^(i) / Σ_j w'^(j)
    4. Resample: Sample N new particles from {(s'^(i), w̃^(i))} to prevent weight degeneracy
    """

    def __init__(
        self,
        num_particles: int = 1000,
        opponent_policy: Optional[Policy] = None,
        resample_threshold: float = 0.5,
    ):
        """
        Args:
            num_particles: Number of particles N
            opponent_policy: Policy π_2 for opponent (used in prediction step)
            resample_threshold: Effective sample size threshold for resampling
        """
        self.num_particles = num_particles
        self.opponent_policy = opponent_policy
        self.resample_threshold = resample_threshold
        self.particles: list[Particle] = []

    def initialize_uniform(
        self, observation: Observation, all_cards: list[Card]
    ) -> None:
        """
        Initialize belief uniformly over states consistent with observation.

        From MATH.md §8.2: Initial belief is uniform over all consistent deals.

        Args:
            observation: Initial observation o_0
            all_cards: Full deck K
        """
        from .marginals import compute_unseen_pool, sample_opponent_hand_uniform

        # Compute unseen pool
        unseen_pool = compute_unseen_pool(
            observation.hand_1, observation.discard, all_cards
        )

        # Sample N particles uniformly
        self.particles = []
        for _ in range(self.num_particles):
            # Sample opponent hand uniformly from unseen pool
            opponent_hand = sample_opponent_hand_uniform(
                unseen_pool, observation.opponent_hand_size
            )

            # Remaining cards go to deck
            deck = [card for card in unseen_pool if card not in opponent_hand]

            # Create state consistent with observation
            state = GameState(
                hand_1=observation.hand_1.copy(),
                hand_2=opponent_hand,
                deck=deck,
                discard=observation.discard.copy(),
                top_card=observation.top_card,
                turn=1,  # Player 1's turn (from perspective)
                draw_penalty=observation.draw_penalty,
            )

            # Uniform weight
            self.particles.append(Particle(state, 1.0 / self.num_particles))

    def predict(self, action: Action) -> None:
        """
        Prediction step: propagate particles through Player 1's action.

        For each particle s^(i), sample successor state s'^(i) ~ P(· | s^(i), a_t)

        Args:
            action: Player 1's action a_t
        """
        new_particles = []

        for particle in self.particles:
            try:
                # Apply Player 1's action (may have stochasticity from drawing)
                new_state = apply_action(particle.state, action)
                new_particles.append(Particle(new_state, particle.weight))
            except Exception:
                # If action fails (e.g., insufficient cards), particle gets zero weight
                # We keep it for now but it will be filtered in update
                continue

        self.particles = new_particles

    def update_opponent_response(self, observation: Observation) -> None:
        """
        Update step: simulate opponent's response and weight by observation.

        This combines:
        1. Opponent action selection via policy π_2
        2. Transition through opponent action
        3. Weighting by observation likelihood

        Args:
            observation: Observation after opponent's turn o_{t+1}
        """
        new_particles = []

        for particle in self.particles:
            # Check if it's opponent's turn in this particle
            if particle.state.turn == 2:
                try:
                    # Opponent selects action
                    if self.opponent_policy:
                        opponent_action = self.opponent_policy.select_action(
                            particle.state
                        )
                    else:
                        # Fallback: draw if penalty, else uniform over legal actions
                        from ..game import get_legal_actions

                        legal_actions = get_legal_actions(particle.state)
                        opponent_action = random.choice(legal_actions)

                    # Apply opponent action
                    new_state = apply_action(particle.state, opponent_action)

                    # Weight by observation likelihood
                    weight = particle.weight * self._observation_likelihood(
                        new_state, observation
                    )

                    if weight > 0:
                        new_particles.append(Particle(new_state, weight))

                except Exception:
                    # Particle incompatible with observation
                    continue
            else:
                # Shouldn't happen, but keep particle as is
                new_particles.append(particle)

        if not new_particles:
            # All particles have zero weight - belief is degenerate
            # Keep old particles with equal weight as fallback
            total_weight = sum(p.weight for p in self.particles)
            if total_weight > 0:
                for p in self.particles:
                    p.weight = 1.0 / len(self.particles)
            return

        # Normalize weights
        total_weight = sum(p.weight for p in new_particles)
        if total_weight > 0:
            for p in new_particles:
                p.weight /= total_weight

        self.particles = new_particles

        # Resample if needed
        if self._effective_sample_size() < self.resample_threshold * self.num_particles:
            self._resample()

    def _observation_likelihood(
        self, state: GameState, observation: Observation
    ) -> float:
        """
        Compute P(o | s) = 𝟙[proj(s) = o]

        Observation is deterministic projection of state.

        Args:
            state: Complete state
            observation: Observation

        Returns:
            1.0 if state consistent with observation, 0.0 otherwise
        """
        # Check all observable components match
        if len(state.hand_1) != len(observation.hand_1):
            return 0.0
        if set(c.id for c in state.hand_1) != set(c.id for c in observation.hand_1):
            return 0.0
        if len(state.hand_2) != observation.opponent_hand_size:
            return 0.0
        if len(state.deck) != observation.deck_size:
            return 0.0
        if len(state.discard) != len(observation.discard):
            return 0.0
        if set(c.id for c in state.discard) != set(c.id for c in observation.discard):
            return 0.0
        if state.top_card.card.id != observation.top_card.card.id:
            return 0.0
        if state.top_card.declared_color != observation.top_card.declared_color:
            return 0.0
        if state.draw_penalty != observation.draw_penalty:
            return 0.0

        return 1.0

    def _effective_sample_size(self) -> float:
        """
        Compute effective sample size: ESS = 1 / Σ_i (w^(i))^2

        Used to determine when resampling is needed.
        """
        if not self.particles:
            return 0.0

        sum_squared_weights = sum(p.weight**2 for p in self.particles)
        if sum_squared_weights == 0:
            return 0.0

        return 1.0 / sum_squared_weights

    def _resample(self) -> None:
        """
        Resample N particles from current weighted set to prevent degeneracy.

        Uses systematic resampling for low variance.
        """
        if not self.particles:
            return

        # Systematic resampling
        N = self.num_particles
        weights = [p.weight for p in self.particles]

        # Generate N evenly spaced points with random start
        positions = [(random.random() + i) / N for i in range(N)]

        # Resample
        new_particles = []
        cumsum = 0.0
        i = 0

        for pos in positions:
            while cumsum < pos and i < len(self.particles):
                cumsum += weights[i]
                i += 1

            if i > 0:
                # Copy particle (create new state copy)
                selected = self.particles[i - 1]
                new_particles.append(
                    Particle(state=selected.state.copy(), weight=1.0 / N)
                )

        self.particles = new_particles

    def get_expected_state(self) -> Optional[GameState]:
        """
        Get expected state (most likely particle).

        Returns particle with highest weight, or None if no particles.
        """
        if not self.particles:
            return None

        return max(self.particles, key=lambda p: p.weight).state

    def sample_state(self) -> GameState:
        """
        Sample a state from the belief distribution.

        Returns:
            Sampled state
        """
        if not self.particles:
            raise ValueError("No particles in belief")

        # Sample according to weights
        states = [p.state for p in self.particles]
        weights = [p.weight for p in self.particles]

        return random.choices(states, weights=weights, k=1)[0]
