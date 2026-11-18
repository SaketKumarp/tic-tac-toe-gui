"""Simple two-player Tic Tac Toe game using Tkinter."""

import tkinter as tk
from tkinter import messagebox

# Game data
board = [""] * 9
current_player = "X"
scores = {"X": 0, "O": 0}
buttons = []

# Every possible winning combination
WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
    (0, 4, 8), (2, 4, 6)              # Diagonals
]


def check_winner():
    """Return X or O if a player has won; otherwise return None."""
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None


def update_score():
    """Show the current score."""
    score_label.config(
        text=f"Player X: {scores['X']}     Player O: {scores['O']}"
    )


def make_move(index):
    """Handle a click on one of the nine board buttons."""
    global current_player

    # Ignore occupied cells and clicks after the game has ended.
    if board[index] != "" or check_winner() or "" not in board:
        return

    board[index] = current_player
    buttons[index].config(
        text=current_player,
        state="disabled",
        disabledforeground="#e8e8e8"
    )

    winner = check_winner()

    if winner:
        scores[winner] += 1
        update_score()
        status_label.config(text=f"Player {winner} wins!")
        disable_board()
    elif "" not in board:
        status_label.config(text="It's a draw!")
        disable_board()
    else:
        current_player = "O" if current_player == "X" else "X"
        status_label.config(text=f"Player {current_player}'s turn")


def disable_board():
    """Disable all cells when the game is finished."""
    for button in buttons:
        button.config(state="disabled")


def new_game():
    """Reset the board while keeping the score."""
    global board, current_player

    board = [""] * 9
    current_player = "X"

    for button in buttons:
        button.config(text="", state="normal")

    status_label.config(text="Player X's turn")


# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("360x460")
root.resizable(False, False)
root.configure(bg="#20252b")

# Heading
title_label = tk.Label(
    root, text="TIC TAC TOE",
    font=("Arial", 24, "bold"),
    bg="#20252b", fg="white"
)
title_label.pack(pady=15)

# Turn / result message
status_label = tk.Label(
    root, text="Player X's turn",
    font=("Arial", 14, "bold"),
    bg="#20252b", fg="#f1c40f"
)
status_label.pack(pady=8)

# 3-by-3 button board
board_frame = tk.Frame(root, bg="#20252b")
board_frame.pack(pady=10)

for i in range(9):
    button = tk.Button(
        board_frame,
        text="",
        font=("Arial", 28, "bold"),
        width=4,
        height=2,
        bg="#3b424a",
        activebackground="#59636e",
        fg="white",
        command=lambda index=i: make_move(index)
    )
    button.grid(row=i // 3, column=i % 3, padx=4, pady=4)
    buttons.append(button)

# Score
score_label = tk.Label(
    root, text="Player X: 0     Player O: 0",
    font=("Arial", 13, "bold"),
    bg="#20252b", fg="white"
)
score_label.pack(pady=12)

# New Game button
new_game_button = tk.Button(
    root, text="New Game",
    font=("Arial", 12, "bold"),
    bg="#27ae60", fg="white",
    activebackground="#219150",
    command=new_game
)
new_game_button.pack(pady=8)

root.mainloop()
