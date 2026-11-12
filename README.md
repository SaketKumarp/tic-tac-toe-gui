# Tic Tac Toe GUI 🎮

A polished desktop Tic Tac Toe game built with **Python**, **CustomTkinter**, and a computer opponent powered by **minimax with alpha-beta pruning**.

## Features

- Player vs Player and Player vs Computer modes
- Easy (random), Medium (win/block), and Hard (minimax + alpha-beta pruning) AI
- Choose X or O and choose who starts
- Custom player names
- Undo, rematch, and return-to-menu controls
- Persistent lifetime scoreboard and recent game history in `scores.json`
- Dark interface, hover feedback, result banner, and animated winning line
- Optional system sound effects
- Separated game rules, AI, UI, and storage modules
- Unit tests with pytest

## Preview

Screenshots and gameplay GIFs can be added to the `assets/` directory.

## Requirements

- Python 3.10+
- Tk support available in your Python installation

## Installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/SaketKumarp/tic-tac-toe-gui.git
cd tic-tac-toe-gui
```

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\\Scripts\\activate    # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Run Tests

```bash
pytest -q
```

## Project Structure

```text
tic-tac-toe-gui/
├── main.py
├── game/
│   ├── __init__.py
│   ├── board.py       # Pure board rules and win/draw detection
│   ├── ai.py          # Easy, Medium, and Hard AI
│   ├── ui.py          # CustomTkinter screens and interaction
│   ├── sounds.py      # Optional system sound helper
│   └── storage.py     # JSON scoreboard and history
├── tests/
│   └── test_board.py
├── assets/
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## How Hard AI Works

Hard mode uses the **minimax** algorithm. It explores possible future moves, scores terminal positions, and chooses the move with the best outcome. **Alpha-beta pruning** skips branches that cannot affect the final decision, reducing the number of positions evaluated. On a standard 3 × 3 board, the search is small enough to run immediately and the AI cannot be forced to lose.

## Saved Data

The game creates `scores.json` in the project root after the first completed match. It stores lifetime X wins, O wins, draws, and the 50 most recent results. This file is intentionally ignored by Git so personal scores stay local.

## Packaging (macOS)

You can build a standalone app with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --windowed --name "TicTacToe" main.py
```

The generated application will be placed in `dist/`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
