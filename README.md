# Tic Tac Toe GUI 🎮

A polished desktop Tic Tac Toe game built with **Python** and **CustomTkinter**. Play against another person or challenge a computer opponent powered by **minimax with alpha-beta pruning**.

## Features

- **Two game modes:** Player vs Player and Player vs Computer
- **Three AI difficulties:**
  - Easy — chooses a random legal move
  - Medium — looks for an immediate win or blocks an opponent's immediate win
  - Hard — uses minimax with alpha-beta pruning; it cannot be forced to lose on the classic 3 × 3 board
- Choose X or O and choose who takes the first turn
- Custom player names
- Undo, rematch, and return-to-menu controls
- Persistent lifetime scoreboard and recent match history in `scores.json`
- Dark interface with hover feedback and animated winning line
- **Win celebration:** animated confetti, a pulsing champion banner, and a generated applause/clapping sound
- Separate draw sound and optional sound-effects toggle
- Cross-platform sound handling for macOS and Windows, with a system-bell fallback
- Modular code structure and pytest unit tests

## Preview

Add screenshots or gameplay recordings to the `assets/` directory and link them here.

## Requirements

- Python 3.10 or newer
- Tk support available in your Python installation
- Dependencies listed in `requirements.txt`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SaketKumarp/tic-tac-toe-gui.git
cd tic-tac-toe-gui
```

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows — Command Prompt**

```bat
py -m venv .venv
.venv\Scripts\activate
```

**Windows — PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Tkinter setup and troubleshooting

CustomTkinter uses Tkinter underneath. Check that Tkinter is available before launching the game:

```bash
python -m tkinter
```

A small Tk test window should appear.

- **macOS with Homebrew Python:** if you see `ModuleNotFoundError: No module named '_tkinter'`, install the matching Tk package. For Python 3.13, run `brew install python-tk@3.13`. If you use another Python version, install the matching `python-tk@<version>` formula. Recreate your virtual environment after installing it.
- **Windows:** install Python from [python.org](https://www.python.org/downloads/windows/) and ensure the Tcl/Tk component is selected. Then recreate the virtual environment if it was created with a different Python installation.
- **Ubuntu / Debian:** install Tk support with `sudo apt install python3-tk` for the system Python you are using.

### VS Code interpreter

If VS Code reports an interpreter error or uses a different Python installation:

1. Open the `tic-tac-toe-gui` folder itself in VS Code.
2. Press `Cmd + Shift + P` on macOS or `Ctrl + Shift + P` on Windows.
3. Choose **Python: Select Interpreter**.
4. Select the interpreter inside this project's `.venv` folder:
   - macOS / Linux: `.venv/bin/python`
   - Windows: `.venv\\Scripts\\python.exe`

In the VS Code terminal, activate the environment and verify it:

```bash
python --version
python -c "import sys; print(sys.executable)"
```

The printed executable path should point to this project's `.venv` directory.

## Run the game

From the project root, with the virtual environment activated:

```bash
python main.py
```

## Run tests

```bash
python -m pytest -q
```

## Project structure

```text
tic-tac-toe-gui/
├── main.py
├── game/
│   ├── __init__.py
│   ├── board.py       # Board state, legal moves, and win/draw detection
│   ├── ai.py          # Easy, Medium, and Hard computer opponents
│   ├── ui.py          # CustomTkinter screens, gameplay, and animations
│   ├── sounds.py      # Generated applause and platform sound playback
│   └── storage.py     # JSON scoreboard and match history
├── tests/
│   └── test_board.py
├── assets/
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## How Hard AI works

Hard mode uses the **minimax** algorithm. It explores possible future moves, scores terminal positions, and chooses the move with the best outcome. **Alpha-beta pruning** skips branches that cannot affect the final decision, reducing the number of positions evaluated. On a standard 3 × 3 board, the search is small enough to run immediately and the AI cannot be forced to lose.

## Saved data

The game creates `scores.json` in the project root after the first completed match. It stores lifetime X wins, O wins, draws, and recent results. This file is intentionally ignored by Git so personal scores stay local.

## Packaging (optional)

You can experiment with building a standalone application using PyInstaller:

```bash
python -m pip install pyinstaller
pyinstaller --windowed --name TicTacToe main.py
```

The generated build will be placed in the `dist/` directory. Build separately on each target operating system.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
