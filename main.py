import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    WINS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)

        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.status = tk.Label(root, font=("Helvetica", 18))
        self.status.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                root,
                text="",
                font=("Helvetica", 40, "bold"),
                width=3,
                height=1,
                command=lambda i=i: self.on_click(i),
            )
            btn.grid(row=1 + i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)

        self.score_label = tk.Label(root, font=("Helvetica", 14))
        self.score_label.grid(row=4, column=0, columnspan=3, pady=5)

        tk.Button(root, text="New Game", font=("Helvetica", 14),
                  command=self.reset).grid(row=5, column=0, columnspan=3, pady=(0, 10))

        self.reset()

    def reset(self):
        self.board = [""] * 9
        self.current = "X"
        self.game_over = False
        for btn in self.buttons:
            btn.config(text="", fg="black")
        self.update_labels()

    def update_labels(self):
        self.status.config(text=f"Player {self.current}'s turn")
        s = self.scores
        self.score_label.config(
            text=f"X: {s['X']}   O: {s['O']}   Draws: {s['Draw']}"
        )

    def on_click(self, i):
        if self.game_over or self.board[i]:
            return

        self.board[i] = self.current
        color = "#d62728" if self.current == "X" else "#1f77b4"
        self.buttons[i].config(text=self.current, fg=color)

        combo = self.get_winning_combo()
        if combo:
            self.game_over = True
            for idx in combo:
                self.buttons[idx].config(fg="#2ca02c")  # green for winners
            self.scores[self.current] += 1
            self.update_labels()
            messagebox.showinfo("Game Over", f"Player {self.current} wins!")
        elif all(self.board):
            self.game_over = True
            self.scores["Draw"] += 1
            self.update_labels()
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            self.current = "O" if self.current == "X" else "X"
            self.update_labels()

    def get_winning_combo(self):
        for a, b, c in self.WINS:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return (a, b, c)
        return None


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()