
# R-R Game - Main entry point
# Run simulations.

from rr_board import RRBoard, PLAYER_X, PLAYER_O
from rr_player_random import RRPlayerRandom
from rr_player_heuristic import RRPlayerHeuristic
from rr_player_minimax import RRPlayerMinimax


NUM_GAMES = 100  # games per matchup


def run_simulation(player_a_cls, player_b_cls, num_games=NUM_GAMES, verbose=False):
    # Run num_games between player_a (X) and player_b (O); alternate who starts
    wins_a = wins_b = draws = 0
    for i in range(num_games):
        if i % 2 == 0:  # even game: A is X, B is O
            pa, pb = player_a_cls(PLAYER_X), player_b_cls(PLAYER_O)
            first, second = pa, pb
        else:  # odd game: swap colors so each side starts 50% of the time
            pa, pb = player_a_cls(PLAYER_O), player_b_cls(PLAYER_X)
            first, second = pb, pa
        board = RRBoard(opening_variant=i % 2)  # alternate opening setup
        current = first
        moves = 0
        while not board.is_game_over() and moves < 300:  # cap at 300 moves
            current.move(board)
            moves += 1
            current = second if current is first else first  # alternate turns
        w = board.get_winner()
        if w is None:  # tie
            draws += 1
        elif (i % 2 == 0 and w == PLAYER_X) or (i % 2 == 1 and w == PLAYER_O):
            wins_a += 1  # A had winning color
        else:
            wins_b += 1
        if verbose and (i + 1) % 10 == 0:  # progress every 10 games
            print(f"  Game {i + 1}/{num_games}: A {wins_a} | B {wins_b} | draws {draws}")
    return wins_a, wins_b, draws


def main():
    n = NUM_GAMES
    print(f"Running simulations ({n} games per matchup)...\n")
    matchups = [  # (name_a, name_b, class_a, class_b)
        ("Random", "Heuristic", RRPlayerRandom, RRPlayerHeuristic),
        ("Heuristic", "Minimax", RRPlayerHeuristic, RRPlayerMinimax),
        ("Random", "Minimax", RRPlayerRandom, RRPlayerMinimax),

        # Checking the fairness of RR by comparing the same player against itself 
        ("Random", "Random", RRPlayerRandom, RRPlayerRandom), 
        ("Heuristic", "Heuristic", RRPlayerHeuristic, RRPlayerHeuristic), 
        ("Minimax", "Minimax", RRPlayerMinimax, RRPlayerMinimax), 
    ]
    results = []
    for name_a, name_b, cls_a, cls_b in matchups:
        print(f"{name_a} vs {name_b}...")
        wa, wb, _ = run_simulation(cls_a, cls_b, n, verbose=True)
        ra, rb = wa / n, wb / n  # win rates 0..1
        results.append((name_a, name_b, ra, rb))
        print(f"  {name_a}: {ra:.2f}, {name_b}: {rb:.2f}\n")

    print("Win Rate Table:")  # summary of all matchups
    print("-" * 55)
    print(f"{'Player A':<12} {'A wins':<12} {'Player B':<12} {'B wins'}")
    print("-" * 55)
    for name_a, name_b, ra, rb in results:
        print(f"{name_a:<12} {ra:<12.2f} {name_b:<12} {rb:.2f}")


if __name__ == "__main__":
    main()
