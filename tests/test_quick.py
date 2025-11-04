#!/usr/bin/env python3
"""
Quick validation test for UNO POMDP implementation.

Run this script to verify the implementation is working correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import UNOPOMDP, HeuristicPolicy, generate_deck, Color


def main():
    print("\n" + "=" * 60)
    print("UNO POMDP - Quick Validation Test")
    print("=" * 60)

    # Test 1: Deck generation
    print("\n[Test 1] Deck Generation")
    deck = generate_deck()
    print(f"✓ Generated deck with {len(deck)} cards")
    assert len(deck) == 108, "Deck should have 108 cards"

    # Verify deck composition
    color_counts = {color: 0 for color in Color}
    wild_count = 0
    for card in deck:
        if card.is_wild():
            wild_count += 1
        else:
            color_counts[card.color] += 1

    print(f"  - Red: {color_counts[Color.RED]}")
    print(f"  - Yellow: {color_counts[Color.YELLOW]}")
    print(f"  - Blue: {color_counts[Color.BLUE]}")
    print(f"  - Green: {color_counts[Color.GREEN]}")
    print(f"  - Wild: {wild_count}")

    # Test 2: POMDP initialization
    print("\n[Test 2] POMDP Initialization")
    pomdp = UNOPOMDP(
        discount=0.95,
        opponent_policy=HeuristicPolicy(randomness=0.1),
        num_particles=100,
    )
    print("✓ Created POMDP instance")

    # Test 3: Game initialization
    print("\n[Test 3] Game Initialization")
    state, obs = pomdp.initialize_game()
    print("✓ Initialized game:")
    print(f"  - Player 1 hand: {len(state.hand_1)} cards")
    print(f"  - Player 2 hand: {len(state.hand_2)} cards")
    print(f"  - Deck: {len(state.deck)} cards")
    print(f"  - Discard: {len(state.discard)} cards")
    print(
        f"  - Top card: {state.top_card.card.color.value if state.top_card.card.color else 'Wild'} {state.top_card.card.rank.value}"
    )

    assert len(state.hand_1) == 7, "Player 1 should have 7 cards"
    assert len(state.hand_2) == 7, "Player 2 should have 7 cards"

    # Test 4: Action selection
    print("\n[Test 4] Action Selection")
    action = pomdp.get_player_1_action()
    print(f"✓ AI selected action: {action}")

    # Test 5: Game step
    print("\n[Test 5] Game Step Execution")
    new_state, new_obs, reward, done, opponent_action = pomdp.step_player_1(action)
    print("✓ Executed action:")
    print(f"  - Reward: {reward}")
    print(f"  - Game over: {done}")
    print(f"  - New state turn: Player {new_state.turn}")
    if opponent_action:
        print(f"  - Opponent played: {opponent_action}")

    # Test 6: Quick game simulation
    print("\n[Test 6] Full Game Simulation")
    pomdp2 = UNOPOMDP(
        discount=0.95,
        opponent_policy=HeuristicPolicy(randomness=0.1),
        num_particles=100,
    )
    winner, num_turns = pomdp2.play_full_game(verbose=False)
    print("✓ Completed full game:")
    print(f"  - Winner: Player {winner if winner > 0 else 'Draw'}")
    print(f"  - Turns: {num_turns}")

    # Success
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print("\nThe UNO POMDP implementation is working correctly.")
    print("Run 'python main.py' to play against the AI.")
    print()


if __name__ == "__main__":
    main()
