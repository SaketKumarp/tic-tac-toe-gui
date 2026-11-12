"""Computer opponents: random, tactical, and minimax with alpha-beta pruning."""

from __future__ import annotations

import random
from typing import Optional

from game.board import GameBoard, O, X

EASY = "Easy"
MEDIUM = "Medium"
HARD = "Hard"
DIFFICULTIES = (EASY, MEDIUM, HARD)


def choose_move(board: GameBoard, difficulty: str = HARD, ai_player: Optional[str] = None) -> int:
    """Choose a legal move for the computer on a copy of the current position."""
    moves = board.available_moves()
    if not moves:
        raise ValueError("No legal moves are available.")
    player = ai_player or board.current_player
    if player != board.current_player:
        raise ValueError("AI can only move when it is the current player's turn.")
    if difficulty == EASY:
        return random.choice(moves)
    if difficulty == MEDIUM:
        return _tactical_move(board, player)
    if difficulty == HARD:
        if board.size != 3 or board.win_length != 3:
            raise ValueError("Hard minimax currently supports the classic 3x3 game.")
        return _minimax_move(board, player)
    raise ValueError(f"Unknown difficulty: {difficulty}")


def _tactical_move(board: GameBoard, player: str) -> int:
    """Win immediately, otherwise block an immediate opponent win, else play randomly."""
    opponent = O if player == X else X
    for candidate in board.available_moves():
        trial = board.clone()
        trial.make_move(candidate)
        if trial.winner == player:
            return candidate
    for candidate in board.available_moves():
        trial = board.clone()
        trial.current_player = opponent
        trial.make_move(candidate)
        if trial.winner == opponent:
            return candidate
    preferred = [4, 0, 2, 6, 8, 1, 3, 5, 7]
    ranked = [index for index in preferred if index in board.available_moves()]
    return ranked[0] if ranked else random.choice(board.available_moves())


def _minimax_move(board: GameBoard, player: str) -> int:
    """Find an optimal move using minimax and alpha-beta pruning."""
    opponent = O if player == X else X
    best_score = float("-inf")
    best_moves: list[int] = []
    alpha, beta = float("-inf"), float("inf")
    for move in board.available_moves():
        trial = board.clone()
        trial.make_move(move)
        score = _minimax(trial, player, opponent, depth=1, alpha=alpha, beta=beta)
        if score > best_score:
            best_score, best_moves = score, [move]
        elif score == best_score:
            best_moves.append(move)
        alpha = max(alpha, best_score)
    return random.choice(best_moves)


def _minimax(board: GameBoard, ai: str, opponent: str, depth: int,
             alpha: float, beta: float) -> float:
    if board.winner == ai:
        return 10 - depth
    if board.winner == opponent:
        return depth - 10
    if board.is_draw:
        return 0

    maximizing = board.current_player == ai
    if maximizing:
        value = float("-inf")
        for move in board.available_moves():
            child = board.clone()
            child.make_move(move)
            value = max(value, _minimax(child, ai, opponent, depth + 1, alpha, beta))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value

    value = float("inf")
    for move in board.available_moves():
        child = board.clone()
        child.make_move(move)
        value = min(value, _minimax(child, ai, opponent, depth + 1, alpha, beta))
        beta = min(beta, value)
        if beta <= alpha:
            break
    return value
