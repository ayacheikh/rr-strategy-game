# Minimax player for R-R game 

import math
import random

from rr_board import RRBoard, PLAYER_X, PLAYER_O, EMPTY, ROWS, COLS


class RRPlayerMinimax:
    # Uses minimax with configurable depth to choose moves

    def __init__(self, player_num, depth=2):
        self.player_num = player_num
        self.opponent = PLAYER_O if player_num == PLAYER_X else PLAYER_X
        self.depth = depth  # search depth (plies)

    def move(self, board):  # pick move via minimax
        # Pick move using minimax 
        valid_moves = board.get_valid_moves(self.player_num)
        if not valid_moves:
            board.apply_pass(self.player_num)
            return
        can_remove = not board.last_move_was_remove.get(self.player_num, False)  # can't remove 2x in a row
        best_moves = []
        best_score = float("-inf")
        for row, col in valid_moves:
            for use_remove in ([False, True] if can_remove else [False]):
                board.apply_move(row, col, use_remove, self.player_num, _skip_validate=True)
                score = self._minimax(board, self.depth - 1, False)  # opponent's turn
                board.undo_move()
                if score > best_score:
                    best_score = score
                    best_moves = [(row, col, use_remove)]
                elif score == best_score:
                    best_moves.append((row, col, use_remove))
        row, col, use_remove = random.choice(best_moves)  # tie-break randomly
        board.apply_move(row, col, use_remove, self.player_num)

    def _minimax(self, board, depth, maximizing, alpha=float("-inf"), beta=float("inf")):
        if depth == 0:  # leaf: use heuristic
            return self._score(board)
        if board.is_game_over():  # terminal: win/loss/tie
            w = board.get_winner()
            if w == self.player_num:
                return 10000
            if w == self.opponent:
                return -10000
            return 0  # tie
        player = board.current_player
        valid_moves = board.get_valid_moves(player)
        if not valid_moves:  # pass
            board.apply_pass(player)
            result = self._minimax(board, depth - 1, not maximizing, alpha, beta)
            board.undo_pass()
            return result
        can_remove = not board.last_move_was_remove.get(player, False)
        is_max = maximizing == (player == self.player_num)  # we maximize, opponent minimizes
        best = float("-inf") if is_max else float("inf")
        for row, col in valid_moves:
            for use_remove in ([False, True] if can_remove else [False]):
                board.apply_move(row, col, use_remove, player, _skip_validate=True)
                s = self._minimax(board, depth - 1, not maximizing, alpha, beta)
                board.undo_move()
                if is_max:  # our turn
                    best = max(best, s)
                    alpha = max(alpha, best)
                else:  # opponent's turn
                    best = min(best, s)
                    beta = min(beta, best)
                if beta <= alpha:  # alpha-beta cutoff
                    break
            if beta <= alpha:
                break  # prune sibling moves
        return best

    def _score(self, board):  # piece differential (from our perspective)
        # Heuristic for non-terminal positions 
        count_x, count_o = board.get_counts()
        count_me = count_x if self.player_num == PLAYER_X else count_o
        count_opp = count_o if self.player_num == PLAYER_X else count_x
        return 10 * (count_me - count_opp)  # simple evaluation
