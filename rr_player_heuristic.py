# Heuristic player for R-R game. Uses evaluation to pick best move

import random

from rr_board import RRBoard, PLAYER_X, PLAYER_O, EMPTY, ROWS, COLS


class RRPlayerHeuristic:
    # Uses position evaluation to choose moves

    def __init__(self, player_num):
        self.player_num = player_num
        self.opponent = PLAYER_O if player_num == PLAYER_X else PLAYER_X

    def move(self, board):  # pick best move by evaluation score
        # Pick the best move according to heuristic score 
        valid_moves = board.get_valid_moves(self.player_num)
        if not valid_moves:
            board.apply_pass(self.player_num)
            return
        can_remove = not board.last_move_was_remove.get(self.player_num, False)  # can't remove 2x in a row
        best_moves = []
        best_score = float("-inf")
        for row, col in valid_moves:
            for use_remove in ([False, True] if can_remove else [False]):  # try both flip and remove
                board.apply_move(row, col, use_remove, self.player_num, _skip_validate=True)
                score = self._score(board)
                board.undo_move()  # restore for next candidate
                if score > best_score:
                    best_score = score
                    best_moves = [(row, col, use_remove)]
                elif score == best_score:
                    best_moves.append((row, col, use_remove))
        row, col, use_remove = random.choice(best_moves)  # tie-break randomly
        board.apply_move(row, col, use_remove, self.player_num)

    def _score(self, board):
        # Evaluate board from current player's perspective (higher = better) 
        count_x, count_o = board.get_counts()
        count_me = count_x if self.player_num == PLAYER_X else count_o
        count_opp = count_o if self.player_num == PLAYER_X else count_x
        score = 10 * (count_me - count_opp)  # piece differential
       
        corners = [(0, 0), (0, 15), (15, 0), (15, 15)]
        for r, c in corners:
            v = board.board[r][c]
            if v == self.player_num:
                score += 50  # bonus for our corner
            elif v == self.opponent:
                score -= 50  # penalty for opponent corner
        return score
