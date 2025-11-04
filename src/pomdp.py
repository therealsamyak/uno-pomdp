"""
Main POMDP class for 2-player UNO.

Follows MATH.md §14: Summary of POMDP Tuple

M = (S, A, T, R, Ω, O, b_0, γ)
"""

import random
from typing import Optional

from .core import (
    Action,
    Card,
    Color,
    GameState,
    Observation,
    TopCard,
    generate_deck,
)
from .game import apply_action, compute_reward, get_legal_actions
from .models import HeuristicPolicy, Policy
from .solver import OnlinePOMDPPlanner, ValueIterationSolver


class UNOPOMDP:
    """
    2-Player UNO POMDP from Player 1's perspective.

    Components:
    - S: State space (GameState)
    - A: Action space (with legal action function)
    - T: Transition dynamics P(s' | s, a)
    - R: Reward function R(s, a)
    - Ω: Observation space (Observation)
    - O: Observation function P(o | s)
    - b_0: Initial belief distribution
    - γ: Discount factor

    The opponent policy π_2 is part of the environment model embedded in T.
    """

    def __init__(
        self,
        discount: float = 0.95,
        opponent_policy: Optional[Policy] = None,
        num_particles: int = 1000,
    ):
        """
        Args:
            discount: Discount factor γ
            opponent_policy: Opponent policy π_2 (if None, uses heuristic)
            num_particles: Number of particles for belief tracking
        """
        self.discount = discount
        self.opponent_policy = opponent_policy or HeuristicPolicy(randomness=0.1)
        self.num_particles = num_particles

        # Full deck K
        self.all_cards = generate_deck()

        # Current state (if simulating)
        self.state: Optional[GameState] = None

        # Planner (for Player 1)
        self.planner: Optional[OnlinePOMDPPlanner] = None

    def initialize_game(self) -> tuple[GameState, Observation]:
        """
        Initialize game state following MATH.md §8.1.

        Initial setup:
        1. Shuffle deck K uniformly
        2. Deal 7 cards to each player
        3. Draw one card for top (reshuffle if Wild/Wild+4)
        4. Initial state s_0
        5. Initial observation o_0 for Player 1

        Returns:
            Tuple of (initial_state, initial_observation)
        """
        from .core import Rank

        # Shuffle deck
        deck = self.all_cards.copy()
        random.shuffle(deck)

        # Deal 7 cards to each player
        hand_1 = deck[:7]
        hand_2 = deck[7:14]
        remaining = deck[14:]

        # Draw top card (reshuffle if wild)
        while True:
            top_card = remaining[0]
            remaining = remaining[1:]

            # If wild, reshuffle and redraw
            if top_card.rank in {Rank.WILD, Rank.WILD_DRAW_FOUR}:
                remaining.append(top_card)
                random.shuffle(remaining)
                continue

            break

        # Create initial state
        discard = [top_card]
        top_card_state = TopCard(top_card, top_card.color)

        self.state = GameState(
            hand_1=hand_1,
            hand_2=hand_2,
            deck=remaining,
            discard=discard,
            top_card=top_card_state,
            turn=1,  # Player 1 starts
            draw_penalty=0,
        )

        # Create initial observation for Player 1
        observation = self._create_observation(self.state)

        # Initialize planner
        solver = ValueIterationSolver(
            discount=self.discount, opponent_policy=self.opponent_policy
        )
        self.planner = OnlinePOMDPPlanner(
            solver=solver,
            opponent_policy=self.opponent_policy,
            num_particles=self.num_particles,
        )
        self.planner.initialize(observation, self.all_cards)

        return self.state, observation

    def _create_observation(self, state: GameState) -> Observation:
        """
        Create observation from state (projection function).

        P(o | s) = 𝟙[proj(s) = o]

        Args:
            state: Complete state

        Returns:
            Observation for Player 1
        """
        return Observation(
            hand_1=state.hand_1.copy(),
            opponent_hand_size=len(state.hand_2),
            deck_size=len(state.deck),
            discard=state.discard.copy(),
            top_card=state.top_card,
            draw_penalty=state.draw_penalty,
        )

    def step_player_1(
        self, action: Action
    ) -> tuple[GameState, Observation, float, bool, Optional[Action]]:
        """
        Execute Player 1's action in the environment.

        Args:
            action: Player 1's action

        Returns:
            Tuple of (new_state, observation, reward, done, opponent_action)
            opponent_action is None if opponent didn't act (game ended)
        """
        if self.state is None:
            raise ValueError("Game not initialized")

        if self.state.turn != 1:
            raise ValueError("Not Player 1's turn")

        # Apply Player 1's action
        try:
            new_state = apply_action(self.state, action)
        except Exception as e:
            # Action failed, game ends with penalty
            return self.state, self._create_observation(self.state), -10.0, True, None

        # Check if Player 1 won
        if len(new_state.hand_1) == 0:
            observation = self._create_observation(new_state)
            reward = 1.0
            self.state = new_state
            return new_state, observation, reward, True, None

        # Player 2's turn
        opponent_action = None
        if new_state.turn == 2:
            # Opponent acts
            opponent_action = self.opponent_policy.select_action(new_state)
            try:
                new_state = apply_action(new_state, opponent_action)
            except Exception as e:
                # If action fails, game ends
                pass

        # Create observation and compute reward
        observation = self._create_observation(new_state)
        reward = compute_reward(self.state, action, new_state)
        done = new_state.is_terminal()

        self.state = new_state
        return new_state, observation, reward, done, opponent_action

    def get_player_1_action(self) -> Action:
        """
        Get Player 1's action using the planner.

        Returns:
            Selected action π*(b)
        """
        if self.planner is None:
            raise ValueError("Planner not initialized")

        # Pass actual state so planner uses correct P1 hand
        return self.planner.select_action(self.state)

    def update_belief(self, action: Action, observation: Observation) -> None:
        """
        Update Player 1's belief after action and observation.

        b_{t+1} = τ(b_t, a_t, o_{t+1})

        Args:
            action: Player 1's action
            observation: New observation
        """
        if self.planner is None:
            raise ValueError("Planner not initialized")

        self.planner.update(action, observation)

    def play_full_game(self, verbose: bool = False) -> tuple[int, int]:
        """
        Play a full game with both players using their policies.

        Args:
            verbose: Whether to print game progress

        Returns:
            Tuple of (winner, num_turns)
            winner: 1 if Player 1 wins, 2 if Player 2 wins, 0 if draw
        """
        state, observation = self.initialize_game()

        turn_count = 0
        max_turns = 1000  # Prevent infinite loops

        while not state.is_terminal() and turn_count < max_turns:
            if verbose:
                print(f"\n--- Turn {turn_count + 1} ---")
                print(f"Player 1 hand: {len(state.hand_1)} cards")
                print(f"Player 2 hand: {len(state.hand_2)} cards")
                print(f"Top card: {state.top_card}")

            # Player 1 acts
            action = self.get_player_1_action()

            if verbose:
                print(f"Player 1 plays: {action}")

            state, observation, reward, done, _ = self.step_player_1(action)

            # Update belief
            self.update_belief(action, observation)

            if done:
                break

            turn_count += 1

        # Determine winner
        if len(state.hand_1) == 0:
            winner = 1
        elif len(state.hand_2) == 0:
            winner = 2
        else:
            # Draw or max turns reached
            if len(state.hand_1) < len(state.hand_2):
                winner = 1
            elif len(state.hand_2) < len(state.hand_1):
                winner = 2
            else:
                winner = 0

        if verbose:
            print(f"\n=== Game Over ===")
            print(f"Winner: Player {winner if winner > 0 else 'Draw'}")
            print(f"Turns: {turn_count}")

        return winner, turn_count
