# Random player for R-R game. Chooses uniformly among valid moves 

import random

from rr_board import RRBoard, PLAYER_X, PLAYER_O


class RRPlayerRandom:
    # Makes random valid moves (or passes when required)

    def __init__(self, player_num):
        self.player_num = player_num  # PLAYER_X or PLAYER_O

    def move(self, board):
        """Pick a random valid move or pass."""
        valid_moves = board.get_valid_moves(self.player_num)
        if not valid_moves:
            board.apply_pass(self.player_num)  # must pass when no moves
            return
        row, col = random.choice(valid_moves)  # pick random valid cell
        # Random choice: remove vs reverse (50/50 when both allowed)
        use_remove = random.choice([True, False])
        if use_remove and board.last_move_was_remove.get(self.player_num, False):
            use_remove = False  # can't remove twice in a row
        board.apply_move(row, col, use_remove, self.player_num)
