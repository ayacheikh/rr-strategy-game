# R-R Game Board Implementation

EMPTY = 0       # empty cell
PLAYER_X = 1    # first player
PLAYER_O = 2    # second player

ROWS = 16       # board height
COLS = 16       # board width

DIRECTIONS = [  # 8 directions: right, left, down, up, diagonals
    (0, 1), (0, -1),
    (1, 0), (-1, 0),
    (1, 1), (-1, -1),
    (1, -1), (-1, 1)
]


class RRBoard:

    def __init__(self, opening_variant=0):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]  # 16x16 grid
        self.current_player = PLAYER_X  # X goes first
        self.last_move_was_remove = {PLAYER_X: False, PLAYER_O: False}  # can't remove twice in a row
        self.remove_count = {PLAYER_X: 0, PLAYER_O: 0}
        self.consecutive_passes = 0  # game ends after 2 consecutive passes
        self.move_history = []  # for undo
        self.count_x = 2 
        self.count_o = 2
        self._setup_opening(opening_variant)

    def _setup_opening(self, variant):
        if variant == 0:  
            self.board[7][7] = PLAYER_X
            self.board[7][8] = PLAYER_O
            self.board[8][7] = PLAYER_O
            self.board[8][8] = PLAYER_X
        else: 
            self.board[7][7] = PLAYER_O
            self.board[7][8] = PLAYER_X
            self.board[8][7] = PLAYER_X
            self.board[8][8] = PLAYER_O

    def _get_opponent(self, player):
        return PLAYER_O if player == PLAYER_X else PLAYER_X

    def _in_bounds(self, r, c):
        return 0 <= r < ROWS and 0 <= c < COLS  # row and col within grid

    def get_valid_moves(self, player=None):
        if player is None:
            player = self.current_player

        opp = self._get_opponent(player)
        moves = set() 

        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != opp:
                    continue  # start from opponent's piece
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if not self._in_bounds(nr, nc):
                        continue
                    if self.board[nr][nc] == EMPTY and (nr, nc) not in moves:
                        if self._get_bracketed_tiles(nr, nc, player):  # must bracket at least one
                            moves.add((nr, nc))

        return list(moves) # list of valid moves

    def must_pass(self, player=None):
        return len(self.get_valid_moves(player)) == 0  # no legal moves


    # Helper func to get titles that are bracketed 
    def _get_bracketed_tiles(self, row, col, player):
        opp = self._get_opponent(player)
        bracketed = set()

        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            path = []
            while self._in_bounds(r, c) and self.board[r][c] == opp:  # follow line of opponent piece
                path.append((r, c))
                r += dr
                c += dc
            if path and self._in_bounds(r, c) and self.board[r][c] == player:  # closed by our piece
                bracketed.update(path)

        return bracketed # set of bracketed tiles

    def apply_move(self, row, col, use_remove, player=None, *, _skip_validate=False):
        if player is None:
            player = self.current_player

        opp = self._get_opponent(player)
        bracketed = self._get_bracketed_tiles(row, col, player)

        if not _skip_validate:
            moves = self.get_valid_moves(player)
            if (row, col) not in moves or not bracketed:
                return False
            if use_remove and self.last_move_was_remove[player]:
                return False  # can't remove twice in a row

        prev_remove = self.last_move_was_remove[player]  # save for undo

        self.board[row][col] = player  # place piece
        if player == PLAYER_X:
            self.count_x += 1
        else:
            self.count_o += 1

        n = len(bracketed)
        if use_remove:  # remove bracketed opponent pieces
            if opp == PLAYER_X:
                self.count_x -= n
            else:
                self.count_o -= n
            for r, c in bracketed:
                self.board[r][c] = EMPTY
            self.last_move_was_remove[player] = True
            self.remove_count[player] += 1
        else:  # flip bracketed stones to our color
            for r, c in bracketed:
                self.board[r][c] = player
            if player == PLAYER_X:
                self.count_x += n
                self.count_o -= n
            else:
                self.count_o += n
                self.count_x -= n
            self.last_move_was_remove[player] = False

        self.current_player = opp  # switch turn
        self.consecutive_passes = 0  # reset pass counter
        self.move_history.append(
            ((row, col), use_remove, player, frozenset(bracketed), prev_remove)
        )
        return True

    def undo_move(self):
        if not self.move_history:
            return False

        entry = self.move_history.pop()
        if entry[0] is None:
            return False

        (row, col), use_remove, player, bracketed, prev_remove = entry
        opp = self._get_opponent(player)

        self.board[row][col] = EMPTY  # remove placed piece
        if player == PLAYER_X:
            self.count_x -= 1
        else:
            self.count_o -= 1

        n = len(bracketed)
        for r, c in bracketed:
            self.board[r][c] = opp  # restore bracketed pieces to opponent

        if use_remove:  # undo the remove
            if opp == PLAYER_X:
                self.count_x += n
            else:
                self.count_o += n
            self.remove_count[player] -= 1
        else:  # undo flip
            if opp == PLAYER_X:
                self.count_x += n
                self.count_o -= n
            else:
                self.count_o += n
                self.count_x -= n

        self.last_move_was_remove[player] = prev_remove
        self.current_player = player  # revert to the original player
        return True

    def apply_pass(self, player=None):
        if player is None:
            player = self.current_player
        self.consecutive_passes += 1
        self.current_player = self._get_opponent(player)  # pass turn
        self.move_history.append((None, None, player))  # None means a pass
        return True

    def undo_pass(self):
        if not self.move_history:
            return False
        entry = self.move_history.pop()
        if entry[0] is not None:
            self.move_history.append(entry)
            return False
        _, _, player = entry
        self.consecutive_passes -= 1
        self.current_player = player
        return True

    def copy(self):
        b = RRBoard.__new__(RRBoard)  # create without calling __init__
        b.board = [row[:] for row in self.board]  # shallow copy of rows
        b.current_player = self.current_player
        b.last_move_was_remove = dict(self.last_move_was_remove)
        b.remove_count = dict(self.remove_count)
        b.consecutive_passes = self.consecutive_passes
        b.move_history = list(self.move_history)
        b.count_x = self.count_x
        b.count_o = self.count_o
        return b

    def _is_full(self):
        return (self.count_x + self.count_o) == ROWS * COLS

    def is_game_over(self):
        if self.consecutive_passes >= 2:  # both players passed
            return True
        if self.count_x == 0 or self.count_o == 0:  # one side eliminated
            return True
        if self._is_full():  # check if board is full
            return True
        if not self.must_pass(self.current_player):
            return False
        return self.must_pass(self._get_opponent(self.current_player))  # both have no moves

    def get_counts(self):
        return self.count_x, self.count_o

    def get_winner(self):
        if self.count_x > self.count_o:
            return PLAYER_X
        if self.count_o > self.count_x:
            return PLAYER_O
        return None  # tie

    def __str__(self):
        header = "  " + " ".join("ABCDEFGHIJKLMNOP")  # column labels
        lines = [header]
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                v = self.board[r][c]
                row.append("." if v == EMPTY else ("X" if v == PLAYER_X else "O"))  # cell chars
            lines.append(f"{r:2} " + " ".join(row))
        return "\n".join(lines)