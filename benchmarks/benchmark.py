#!/usr/bin/env python3
"""
Benchmark script for UNO POMDP solver.

Tests AI vs AI performance with identical policies to explore Nash equilibrium.
"""

import sys
import time
from collections import defaultdict
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import UNOPOMDP, HeuristicPolicy


def run_benchmark(
    num_games: int = 100, num_particles: int = 1000, verbose: bool = False
):
    """
    Run benchmark with AI vs AI using identical policies.

    This tests for Nash equilibrium: if both players use the same policy,
    we expect roughly balanced win rates (around 50-50).

    Args:
        num_games: Number of games to simulate
        num_particles: Number of particles for belief tracking
        verbose: Print detailed output
    """
    print("\n" + "=" * 70)
    print("UNO POMDP Benchmark - Nash Equilibrium Test")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  - Games: {num_games}")
    print(f"  - Particles: {num_particles}")
    print(f"  - Policy: HeuristicPolicy (both players)")
    print(f"  - Discount: 0.95")
    print()

    # Statistics
    wins = defaultdict(int)
    turn_counts = []
    game_times = []

    # Progress tracking
    print("Running games...")
    start_time = time.time()

    for game_num in range(1, num_games + 1):
        if game_num % 10 == 0:
            print(f"  Progress: {game_num}/{num_games} games", end="\r")

        game_start = time.time()

        # Create fresh POMDP for each game
        pomdp = UNOPOMDP(
            discount=0.95,
            opponent_policy=HeuristicPolicy(randomness=0.1),
            num_particles=num_particles,
        )

        # Play game
        winner, turns = pomdp.play_full_game(verbose=False)

        game_time = time.time() - game_start

        # Record stats
        wins[winner] += 1
        turn_counts.append(turns)
        game_times.append(game_time)

        if verbose and game_num <= 5:
            print(
                f"\nGame {game_num}: Player {winner if winner > 0 else 'Draw'} wins in {turns} turns ({game_time:.2f}s)"
            )

    total_time = time.time() - start_time

    # Print results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"\nWin Statistics:")
    print(f"  - Player 1 wins: {wins[1]:3d} ({wins[1] / num_games * 100:5.1f}%)")
    print(f"  - Player 2 wins: {wins[2]:3d} ({wins[2] / num_games * 100:5.1f}%)")
    print(f"  - Draws:         {wins[0]:3d} ({wins[0] / num_games * 100:5.1f}%)")

    print(f"\nGame Length:")
    print(f"  - Average turns: {sum(turn_counts) / len(turn_counts):.1f}")
    print(f"  - Min turns:     {min(turn_counts)}")
    print(f"  - Max turns:     {max(turn_counts)}")

    print(f"\nPerformance:")
    print(f"  - Total time:    {total_time:.1f}s")
    print(f"  - Average/game:  {sum(game_times) / len(game_times):.2f}s")
    print(f"  - Games/second:  {num_games / total_time:.2f}")

    # Nash equilibrium analysis
    print(f"\nNash Equilibrium Analysis:")
    player1_ratio = wins[1] / num_games
    player2_ratio = wins[2] / num_games
    balance_metric = abs(player1_ratio - player2_ratio)

    print(f"  - Win rate difference: {balance_metric * 100:.1f}%")

    if balance_metric < 0.1:
        print("  ✓ Policies appear well-balanced (< 10% difference)")
    elif balance_metric < 0.2:
        print("  ~ Policies somewhat balanced (10-20% difference)")
    else:
        print("  ✗ Policies show significant imbalance (> 20% difference)")

    print("\n" + "=" * 70)


def main():
    """Main entry point"""
    import sys

    # Parse arguments
    num_games = 100
    num_particles = 1000
    verbose = False

    if len(sys.argv) > 1:
        try:
            num_games = int(sys.argv[1])
        except ValueError:
            print("Usage: python benchmark.py [num_games] [num_particles] [verbose]")
            sys.exit(1)

    if len(sys.argv) > 2:
        try:
            num_particles = int(sys.argv[2])
        except ValueError:
            print("Usage: python benchmark.py [num_games] [num_particles] [verbose]")
            sys.exit(1)

    if len(sys.argv) > 3:
        verbose = sys.argv[3].lower() in ["true", "yes", "1"]

    run_benchmark(num_games, num_particles, verbose)


if __name__ == "__main__":
    main()
