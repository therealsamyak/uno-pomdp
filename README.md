# UNO POMDP Solver

A complete implementation of 2-player UNO as a Partially Observable Markov Decision Process (POMDP) with particle filter belief tracking and value iteration solver.

## Overview

This project implements the full UNO card game as a POMDP following a rigorous mathematical specification (see `MATH.md`). The implementation includes:

- **Core Game Engine**: Complete UNO rules for 2-player games
- **Belief Tracking**: Particle filter for maintaining belief over opponent's hand
- **Solver**: Value iteration with heuristic approximations
- **CLI Interface**: Play against the AI or watch AI vs AI matches

## Mathematical Foundation

The implementation follows `MATH.md` which defines:

- State space S (hands, deck, discard, top card, turn, metadata)
- Action space A (play actions with color declaration, draw actions)
- Observation space Ω (partial state visible to Player 1)
- Transition dynamics T with opponent model
- Reward function R (win/loss/draw)
- Belief update operators τ (Chapman-Kolmogorov + Bayes)

## Features

### Complete 2-Player UNO Rules

- Standard UNO deck (108 cards: numbered, action, and wild cards)
- 2-player special rules: Reverse acts as Skip, no draw stacking
- Proper reshuffle mechanics when deck runs out
- Wild card color declaration

### POMDP Components

- **State representation**: Full game state with hidden opponent hand
- **Observation model**: Partial observability (opponent hand size only)
- **Belief tracking**: Particle filter with 1000 particles (configurable)
- **Opponent model**: Pluggable policies (uniform, greedy, heuristic)

### AI Solver

- Value iteration in belief space
- Heuristic value approximations:
  - Hand size difference
  - Expected playable cards in opponent hand
  - Wild card count
  - Action card count
  - Color diversity
- Nash equilibrium testing (both players use same policy)

## Installation

```bash
# Using uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Usage

### Interactive Play

Play against the AI:

```bash
python main.py
```

Choose option 1 to play interactively, or option 2/3 to watch AI vs AI games.

### Running Tests

```bash
python tests/test_quick.py
```

### Running Benchmarks

```bash
# Run 100 games with 1000 particles
python benchmarks/benchmark.py 100 1000

# Quick benchmark (5 games, 50 particles)
python benchmarks/benchmark.py 5 50
```

### Programmatic Usage

```python
from src import UNOPOMDP, HeuristicPolicy

# Create POMDP
pomdp = UNOPOMDP(
    discount=0.95,
    opponent_policy=HeuristicPolicy(randomness=0.1),
    num_particles=1000
)

# Play a game
winner, num_turns = pomdp.play_full_game(verbose=True)
print(f"Winner: Player {winner}, Turns: {num_turns}")
```

### Custom Policies

```python
from src import UNOPOMDP, Policy, GameState, Action

class CustomPolicy:
    def select_action(self, state: GameState) -> Action:
        # Your custom logic here
        pass

    def get_action_probability(self, state: GameState, action: Action) -> float:
        # Return probability of selecting action
        pass

pomdp = UNOPOMDP(opponent_policy=CustomPolicy())
```

## Project Structure

```
src/
├── core/           # Game primitives (cards, state, actions, observations)
├── game/           # Game logic (rules, transitions, rewards)
├── models/         # Policy implementations
├── belief/         # Belief tracking (particle filter, marginals)
├── solver/         # Value iteration solver and heuristics
├── cli/            # Command-line interface
└── pomdp.py        # Main POMDP class

tests/              # Test suite
benchmarks/         # Benchmarking and analysis scripts
```

## Implementation Notes

- Uses labeled deck with 108 unique cards (K = {K₁, ..., K₁₀₈})
- Deck and discard pile are multisets (unordered)
- Uniform random sampling for drawing cards
- Particle filter with systematic resampling
- Discount factor γ = 0.95
- Both players can use identical policy for Nash equilibrium analysis

## References

See `MATH.md` for complete mathematical specification including:

- Formal notation and primitive sets
- State space definition
- Action legality constraints
- Transition dynamics
- Observation likelihood
- Belief update equations
- Value function and Bellman optimality

## License

See LICENSE file for details.
