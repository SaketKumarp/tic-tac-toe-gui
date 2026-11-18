"""Entry point for the two-player Tic Tac Toe game."""

import tkinter as tk

from game.ui import TicTacToeApp


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
