# R-R Strategy Game AI

A Python implementation of R-R, a two-player abstract strategy game played on a 16×16 board, inspired by Othello/Reversi. The project includes three AI players of increasing skill — random, heuristic, and minimax — and a simulation runner (`main.py`) to evaluate and compare them.

**Requirements:** Python 3. No third-party packages (stdlib only).

## What is R-R?

R-R is a two-player board game where players (X and O) alternate placing tiles on a 16×16 grid. A move is valid only if it brackets at least one opponent tile — meaning the newly placed tile, combined with an existing tile of the same player, sandwiches one or more opponent tiles in a straight line (horizontal, vertical, or diagonal) with no gaps.

When a player brackets opponent tiles, they choose one of two modes:

- **Reverse Mode** — flip the bracketed opponent tiles to their own color (like Othello)
- **Remove Mode** — remove the bracketed opponent tiles from the board entirely

The player with the most tiles on the board when the game ends wins.

### Advanced Variant

This implementation uses the following advanced variant:

- Each player is not allowed to use Remove Mode twice in a row

## Game Rules Summary

- 16×16 board, opening with four tiles in the center 2×2 block (two per player, diagonal layout)
- Players alternate turns; X plays first
- Each turn: place one tile on an empty square that brackets at least one opponent tile
- Choose Reverse or Remove for all bracketed tiles (cannot mix in the same turn)
- Pass if no legal move exists
- Game ends when: both players pass consecutively, one player has zero tiles, the board is full, or neither player has a legal move

## AI Players

Each player implements a `move(board)` method that either applies a move or passes when no legal moves exist. All players respect the consecutive-remove restriction.

### Random (`rr_player_random.py`)

Chooses a random legal placement, then randomly picks Reverse or Remove (falling back to Reverse if Remove is not allowed). Baseline for comparison.

### Heuristic (`rr_player_heuristic.py`)

For each legal move (and each allowed Reverse/Remove choice), applies the move on a copy of the board, scores the result, and picks the highest-scoring option (random tie-break). The evaluation function uses:

- **Piece differential** — `10 × (my tiles − opponent tiles)`
- **Corner control** — `+50` per corner occupied by the player, `−50` per corner held by the opponent

### Minimax (`rr_player_minimax.py`)

Uses minimax with **alpha–beta pruning** and default **search depth 2**. At leaf nodes, uses the same piece-differential heuristic as above; terminal wins/losses receive large fixed scores. Ties among best moves are broken randomly.

## Simulation Results

`main.py` runs **100 games per matchup**. For fairness, each matchup alternates who plays as X vs O and alternates between two center opening setups. Win rates are reported as the fraction of games won (draws account for the remainder when rates do not sum to 1.0).

| Player A   | Player A Win Rate | Player B   | Player B Win Rate |
|------------|-------------------|------------|-------------------|
| Random     | 0.05              | Heuristic  | 0.93              |
| Heuristic  | 0.53              | Minimax    | 0.45              |
| Random     | 0.01              | Minimax    | 0.99              |

*Results from running `python main.py`.*

## Fairness Analysis

One key question this project explores is whether R-R gives a first-move advantage to X. By alternating starting color and opening variant across simulations, we can see whether one side wins disproportionately when the same AI plays itself.

### Fairness Comparison (Players Against Themselves)

| Player A   | A wins | Player B   | B wins |
|------------|--------|------------|--------|
| Random     | 0.46   | Random     | 0.32   |
| Heuristic  | 0.52   | Heuristic  | 0.46   |
| Minimax    | 0.53   | Minimax    | 0.47   |

**Conclusion:** Random vs Heuristic and Random vs Minimax show the stronger player dominating (0.93–0.99) regardless of who starts. Heuristic vs Minimax is closer (0.53 vs 0.45). In self-play, win rates stay near 50/50 for Heuristic and Minimax; Random self-play is more uneven (0.46 vs 0.32), with the rest of games ending in draws. None of the matchups show a consistent pattern where going first means winning, so R-R does not appear to give a meaningful first-move advantage.

## Project Structure

```
rr-strategy-game/
├── main.py                 # Entry point: runs all matchups and prints win-rate tables
├── rr_board.py             # Board state, bracketing, moves, passes, undo, game-over logic
├── rr_player_random.py     # Random-move AI
├── rr_player_heuristic.py  # Greedy heuristic AI
├── rr_player_minimax.py    # Minimax + alpha-beta AI (default depth 2)
└── README.md
```

| File | Role |
|------|------|
| `rr_board.py` | 16×16 grid, valid-move detection, Reverse/Remove application, pass handling, move history with undo (used by minimax search), winner by tile count |
| `main.py` | `run_simulation()` game loop; six matchups (three cross-player, three self-play); prints progress and summary table |
| `rr_player_*.py` | Player implementations consumed by `main.py` |

## How to Run

```bash
git clone https://github.com/ayacheikh/rr-strategy-game.git
cd rr-strategy-game
python main.py
```

Simulations print progress every 10 games per matchup, then a final win-rate table. There is no interactive human-vs-AI mode in this repo.
