"""
CLI game interface for playing UNO against the AI.
"""

import sys
from typing import Optional

from ..core import Action, Color, DrawAction, PlayAction, create_play_action
from ..game import get_legal_actions
from ..models import HeuristicPolicy
from ..pomdp import UNOPOMDP
from .display import (
    clear_screen,
    display_action,
    display_actions,
    display_compact_state,
    display_game_state,
    display_move_log,
    display_winner,
    format_action,
)


class CLIGameInterface:
    """CLI interface for playing UNO against the AI"""

    def __init__(
        self, player_is_first: bool = True, ai_policy: Optional[HeuristicPolicy] = None
    ):
        """
        Args:
            player_is_first: Whether human player goes first
            ai_policy: Policy for AI opponent
        """
        self.player_is_first = player_is_first
        self.ai_policy = ai_policy or HeuristicPolicy(randomness=0.1)

        # Create POMDP (AI is always Player 1 internally)
        self.pomdp = UNOPOMDP(
            discount=0.95, opponent_policy=self.ai_policy, num_particles=1000
        )

    def play_game(self) -> None:
        """Play a full game with human interaction"""
        print("\n" + "=" * 70)
        print("Welcome to UNO POMDP!")
        print("=" * 70)
        print(
            "\nYou (Player 2) are playing against an AI (Player 1) using POMDP planning."
        )
        print("The AI uses belief tracking and value iteration to play optimally.")
        print("\nLet's begin!\n")

        input("Press Enter to start...")

        # Initialize game
        state, observation = self.pomdp.initialize_game()
        turn_count = 0
        max_turns = 1000
        move_history = []  # Track (player, action, hand_size, turn_number)

        while not state.is_terminal() and turn_count < max_turns:
            clear_screen()

            # Display move history
            if move_history:
                display_move_log(move_history, max_recent=8)

            # Display current state
            display_game_state(observation, turn_player=state.turn)

            # Determine who acts
            if state.turn == 1:
                # AI's turn (Player 1)
                print("\n🤖 AI is thinking...")
                action = self.pomdp.get_player_1_action()

                print()
                display_action(action, 1, "🤖 AI")

                # Execute action
                state, observation, reward, done, opponent_action = (
                    self.pomdp.step_player_1(action)
                )
                self.pomdp.update_belief(action, observation)

                # Log move
                move_history.append((1, action, len(state.hand_1), turn_count + 1))

                # Log opponent move if they acted
                if opponent_action is not None:
                    move_history.append(
                        (2, opponent_action, len(state.hand_2), turn_count + 1)
                    )

                input("\nPress Enter to continue...")

            else:
                # Human's turn (Player 2)
                action = self._get_human_action(state)

                if action is None:
                    # User quit
                    print("\nGame aborted.")
                    return

                print()
                display_action(action, 2, "👤 You")

                # Execute action
                from ..game import apply_action

                try:
                    state = apply_action(state, action)
                    observation = self.pomdp._create_observation(state)
                    self.pomdp.state = state

                    # Log move
                    move_history.append((2, action, len(state.hand_2), turn_count + 1))

                except Exception as e:
                    print(f"\nError applying action: {e}")
                    input("Press Enter to continue...")
                    continue

            turn_count += 1

        # Game over
        clear_screen()

        # Show final move history
        if move_history:
            print("\n" + "=" * 70)
            print("COMPLETE GAME HISTORY")
            print("=" * 70)
            display_move_log(move_history, max_recent=20)

        # Determine winner
        if len(state.hand_1) == 0:
            winner = 1  # AI wins
        elif len(state.hand_2) == 0:
            winner = 2  # Human wins
        else:
            # Draw or max turns
            if len(state.hand_1) < len(state.hand_2):
                winner = 1
            elif len(state.hand_2) < len(state.hand_1):
                winner = 2
            else:
                winner = 0

        display_winner(winner, turn_count)

        if winner == 1:
            print("\n🤖 The AI won! Better luck next time.")
        elif winner == 2:
            print("\n🎉 Congratulations! You beat the AI!")
        else:
            print("\n🤝 It's a draw!")

    def _get_human_action(self, state) -> Optional[Action]:
        """
        Get action from human player.

        Args:
            state: Current game state

        Returns:
            Selected action, or None if user quits
        """
        legal_actions = get_legal_actions(state)

        if not legal_actions:
            print("\nNo legal actions available!")
            return None

        while True:
            print()
            display_actions(legal_actions)
            print("\nEnter action number (or 'q' to quit): ", end="")

            try:
                user_input = input().strip().lower()

                if user_input == "q":
                    return None

                choice = int(user_input)

                if 1 <= choice <= len(legal_actions):
                    return legal_actions[choice - 1]
                else:
                    print(f"Invalid choice. Please enter 1-{len(legal_actions)}.")

            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nGame interrupted.")
                return None


def play_ai_vs_ai(num_games: int = 1, verbose: bool = True) -> None:
    """
    Play games with AI vs AI.

    Args:
        num_games: Number of games to play
        verbose: Whether to print game details
    """
    print(f"\nPlaying {num_games} game(s) with AI vs AI...")
    print("Both players use HeuristicPolicy (testing for Nash equilibrium)")

    wins = {1: 0, 2: 0, 0: 0}
    total_turns = 0

    for game_num in range(1, num_games + 1):
        if verbose:
            print(f"\n{'=' * 70}")
            print(f"GAME {game_num}/{num_games}")
            print("=" * 70)

        pomdp = UNOPOMDP(
            discount=0.95,
            opponent_policy=HeuristicPolicy(randomness=0.1),
            num_particles=1000,
        )

        # Play game with detailed logging
        if verbose:
            winner, turns = _play_ai_vs_ai_verbose(pomdp)
        else:
            winner, turns = pomdp.play_full_game(verbose=False)

        wins[winner] += 1
        total_turns += turns

        if verbose:
            winner_str = f"Player {winner}" if winner > 0 else "Draw"
            print(f"\n{'=' * 70}")
            print(f"Game {game_num} Result: {winner_str} wins in {turns} turns")
            print("=" * 70)

    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print("=" * 70)
    print(f"Games played: {num_games}")
    print(f"Player 1 wins: {wins[1]} ({wins[1] / num_games * 100:.1f}%)")
    print(f"Player 2 wins: {wins[2]} ({wins[2] / num_games * 100:.1f}%)")
    print(f"Draws: {wins[0]} ({wins[0] / num_games * 100:.1f}%)")
    print(f"Average turns: {total_turns / num_games:.1f}")
    print("=" * 70)


def _play_ai_vs_ai_verbose(pomdp: UNOPOMDP) -> tuple[int, int]:
    """
    Play a single AI vs AI game with verbose output.

    Args:
        pomdp: POMDP instance

    Returns:
        Tuple of (winner, num_turns)
    """
    state, observation = pomdp.initialize_game()

    print("\nInitial State:")
    display_compact_state(
        state.top_card,
        len(state.hand_1),
        len(state.hand_2),
        len(state.deck),
        state.draw_penalty,
        state.turn,
    )

    turn_count = 0
    max_turns = 1000
    move_history = []

    while not state.is_terminal() and turn_count < max_turns:
        print(f"\n--- Turn {turn_count + 1} ---")

        # Player 1 acts
        action_p1 = pomdp.get_player_1_action()
        display_action(action_p1, 1, "Player 1")

        # Record state after P1's action (before P2 acts)
        intermediate_state = None
        try:
            from ..game import apply_action

            intermediate_state = apply_action(state, action_p1)
        except:
            pass

        state, observation, reward, done, action_p2 = pomdp.step_player_1(action_p1)
        pomdp.update_belief(action_p1, observation)

        move_history.append(
            (
                1,
                action_p1,
                len(state.hand_1)
                if action_p2
                else intermediate_state.hand_1.count
                if intermediate_state
                else len(state.hand_1),
                turn_count + 1,
            )
        )

        # Show Player 2's action if they acted
        if action_p2 is not None and not done:
            display_action(action_p2, 2, "Player 2")
            move_history.append((2, action_p2, len(state.hand_2), turn_count + 1))

        # Show state after both moves
        display_compact_state(
            state.top_card,
            len(state.hand_1),
            len(state.hand_2),
            len(state.deck),
            state.draw_penalty,
            state.turn,
        )

        if done:
            break

        turn_count += 1

    # Show move history
    if move_history:
        print("\n" + "=" * 70)
        print("MOVE HISTORY")
        print("=" * 70)
        for i, (player, action, hand_size, turn) in enumerate(move_history, 1):
            action_str = format_action(action)
            print(f"  {i}. Player {player}: {action_str} (hand: {hand_size} cards)")

    # Determine winner
    if len(state.hand_1) == 0:
        winner = 1
    elif len(state.hand_2) == 0:
        winner = 2
    else:
        if len(state.hand_1) < len(state.hand_2):
            winner = 1
        elif len(state.hand_2) < len(state.hand_1):
            winner = 2
        else:
            winner = 0

    return winner, turn_count


def main():
    """Main entry point for CLI"""
    print("\nUNO POMDP Solver")
    print("=" * 60)
    print("\nChoose mode:")
    print("1. Play against AI")
    print("2. Watch AI vs AI (single game)")
    print("3. Run AI vs AI benchmark (multiple games)")
    print("q. Quit")

    choice = input("\nEnter choice: ").strip().lower()

    if choice == "1":
        interface = CLIGameInterface(player_is_first=True)
        interface.play_game()

    elif choice == "2":
        play_ai_vs_ai(num_games=1, verbose=True)

    elif choice == "3":
        try:
            num_games = int(input("Number of games: ").strip())
            verbose = input("Verbose output? (y/n): ").strip().lower() == "y"
            play_ai_vs_ai(num_games=num_games, verbose=verbose)
        except ValueError:
            print("Invalid input.")

    elif choice == "q":
        print("Goodbye!")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
