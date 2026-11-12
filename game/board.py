"""Pure Tic Tac Toe game rules, independent of the graphical interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

X = "X"
O = "O"
EMPTY = ""
PLAYERS = (X, O)


@dataclass
class GameBoard:
    """Represent a square Tic Tac Toe board and its game state.

    Args:
        size: Number of rows and columns.
        win_length: Consecutive marks required to win.
    """

    size: int = 3
    win_length: int = 3
    cells: list[str] = field(default_factory=list)
    current_player: str = X
    winner: Optional[str] = None
    winning_combo: Optional[tuple[int, ...]] = None
    move_history: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.size < 3:
            raise ValueError("Board size must be at least 3.")
        if not 3 <= self.win_length <= self.size:
            raise ValueError("win_length must be between 3 and board size.")
        if not self.cells:
            self.cells = [EMPTY] * (self.size * self.size)
        elif len(self.cells) != self.size * self.size:
            raise ValueError("Cell count does not match board dimensions.")

    @property
    def is_over(self) -> bool:
        """Return True when the game has a winner or the board is full."""
        return self.winner is not None or EMPTY not in self.cells

    @property
    def is_draw(self) -> bool:
        """Return True when the board is full and nobody has won."""
        return self.winner is None and EMPTY not in self.cells

    def available_moves(self) -> list[int]:
        """Return the indexes of all empty cells."""
        return [i for i, cell in enumerate(self.cells) if cell == EMPTY]

    def make_move(self, index: int) -> bool:
        """Place the current player's mark. Return False for an invalid move."""
        if not 0 <= index < len(self.cells) or self.is_over or self.cells[index]:
            return False
        player = self.current_player
        self.cells[index] = player
        self.move_history.append(index)
        self.winning_combo = self._find_winning_combo(player)
        if self.winning_combo:
            self.winner = player
        elif EMPTY in self.cells:
            self.current_player = O if player == X else X
        return True

    def undo_move(self) -> Optional[int]:
        """Undo the most recent move and return its index, if one exists."""
        if not self.move_history:
            return None
        index = self.move_history.pop()
        self.cells[index] = EMPTY
        self.winner = None
        self.winning_combo = None
        self.current_player = X if len(self.move_history) % 2 == 0 else O
        return index

    def reset(self, starting_player: str = X) -> None:
        """Clear the board and choose the next starting player."""
        if starting_player not in PLAYERS:
            raise ValueError("starting_player must be X or O.")
        self.cells = [EMPTY] * (self.size * self.size)
        self.current_player = starting_player
        self.winner = None
        self.winning_combo = None
        self.move_history.clear()

    def _find_winning_combo(self, player: str) -> Optional[tuple[int, ...]]:
        """Find a winning row, column, or diagonal for player."""
        n, k = self.size, self.win_length
        lines: list[list[int]] = []
        for r in range(n):
            for c in range(n - k + 1):
                lines.append([r * n + c + j for j in range(k)])
        for c in range(n):
            for r in range(n - k + 1):
                lines.append([(r + j) * n + c for j in range(k)])
        for r in range(n - k + 1):
            for c in range(n - k + 1):
                lines.append([(r + j) * n + c + j for j in range(k)])
                lines.append([(r + j) * n + c + k - 1 - j for j in range(k)])
        for line in lines:
            if all(self.cells[index] == player for index in line):
                return tuple(line)
        return None
