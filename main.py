"""Application entry point for Tic Tac Toe GUI."""

from game.ui import TicTacToeApp


def main() -> None:
    """Create and run the desktop application."""
    app = TicTacToeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
