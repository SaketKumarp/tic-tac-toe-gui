"""Game rules and state for Tic Tac Toe."""


class TicTacToeGame:
    WINNING_COMBINATIONS = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.winner = None
        self.finished = False

    def play(self, position):
        """Play at a zero-based board position and return the move result."""
        if self.finished or not 0 <= position < 9 or self.board[position]:
            return "invalid"

        self.board[position] = self.current_player

        for a, b, c in self.WINNING_COMBINATIONS:
            mark = self.board[a]
            if mark and mark == self.board[b] == self.board[c]:
                self.winner = mark
                self.finished = True
                return "win"

        if all(self.board):
            self.finished = True
            return "draw"

        self.current_player = "O" if self.current_player == "X" else "X"
        return "continue"
