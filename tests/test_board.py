"""Unit tests for board rules and the computer opponent."""

from game.ai import EASY, HARD, MEDIUM, choose_move
from game.board import GameBoard, O, X


def test_horizontal_win() -> None:
    board = GameBoard()
    for move in (0, 3, 1, 4, 2):
        board.make_move(move)
    assert board.winner == X
    assert board.winning_combo == (0, 1, 2)


def test_vertical_win() -> None:
    board = GameBoard()
    for move in (0, 1, 3, 2, 6):
        board.make_move(move)
    assert board.winner == X


def test_diagonal_win() -> None:
    board = GameBoard()
    for move in (0, 1, 4, 2, 8):
        board.make_move(move)
    assert board.winner == X


def test_draw_detection() -> None:
    board = GameBoard()
    for move in (0, 1, 2, 4, 3, 5, 7, 6, 8):
        board.make_move(move)
    assert board.is_draw
    assert board.winner is None


def test_invalid_or_occupied_move_is_rejected() -> None:
    board = GameBoard()
    assert board.make_move(0)
    assert not board.make_move(0)
    assert not board.make_move(9)


def test_undo_restores_previous_player() -> None:
    board = GameBoard()
    board.make_move(0)
    board.make_move(1)
    assert board.undo_move() == 1
    assert board.current_player == O
    assert board.cells[1] == ""


def test_easy_medium_and_hard_return_legal_moves() -> None:
    for difficulty in (EASY, MEDIUM, HARD):
        board = GameBoard()
        move = choose_move(board, difficulty, X)
        assert move in board.available_moves()


def test_hard_ai_takes_winning_move() -> None:
    board = GameBoard()
    board.cells = [X, X, "", O, O, "", "", "", ""]
    board.current_player = X
    assert choose_move(board, HARD, X) == 2


def test_hard_ai_blocks_immediate_loss() -> None:
    board = GameBoard()
    board.cells = [O, O, "", X, "", "", "", "", ""]
    board.current_player = X
    assert choose_move(board, HARD, X) == 2


def test_hard_ai_never_loses_against_any_opponent_reply() -> None:
    """Explore opponent replies while letting Hard AI choose its optimal move."""
    def explore(position: GameBoard) -> bool:
        if position.winner == O:
            return False
        if position.is_over:
            return True
        if position.current_player == X:
            move = choose_move(position, HARD, X)
            next_position = position.clone()
            next_position.make_move(move)
            return explore(next_position)
        for move in position.available_moves():
            next_position = position.clone()
            next_position.make_move(move)
            if not explore(next_position):
                return False
        return True

    assert explore(GameBoard())
