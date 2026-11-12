# Tic Tac Toe GUI

A desktop Tic Tac Toe game built with **Python** and **CustomTkinter**. Play locally with two people on the same computer: Player 1 uses **X** and Player 2 uses **O**.

The game includes a dark interface, animated winning line, confetti celebration, and sound effects for wins and draws.

## Features

- **Two-player gameplay:** Player 1 (X) vs Player 2 (O)
- Custom names for both players
- Choose whether X or O takes the first turn
- Clear turn indicator and win/draw detection
- Undo the most recent move
- Rematch and return-to-menu controls
- Lifetime scoreboard and recent match history saved locally in `scores.json`
- Animated winning line
- Win celebration with falling confetti and a pulsing champion banner
- Generated applause/clapping sound effect for a win
- Separate draw sound and an option to toggle sound effects
- Cross-platform sound playback support for macOS and Windows, with a system-bell fallback
- Modular Python code and unit tests

## Preview

Add screenshots or a short gameplay recording to the `assets/` directory and embed them here:

```md
![Tic Tac Toe gameplay](assets/gameplay.png)
```

## Requirements

- Python 3.10 or newer
- Tkinter support in your Python installation
- Dependencies listed in `requirements.txt`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SaketKumarp/tic-tac-toe-gui.git
cd tic-tac-toe-gui
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows — Command Prompt**

```bat
py -m venv .venv
.venv\\Scripts\\activate
```

**Windows — PowerShell**

```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the game

From the project root, with the virtual environment activated:

```bash
python main.py
```

On Windows, you can also use `py main.py`.

## Tkinter setup and troubleshooting

CustomTkinter uses Tkinter underneath. Verify that Tkinter is available:

```bash
python -m tkinter
```

A small test window should open.

- **macOS with Homebrew Python:** If Python reports `No module named '_tkinter'`, install the matching Tk package. For Python 3.13, run `brew install python-tk@3.13`. Use the formula matching your Python version, then recreate the virtual environment.
- **Windows:** Install Python from [python.org](https://www.python.org/downloads/windows/) and make sure the Tcl/Tk and IDLE option is selected. Recreate the virtual environment if you changed Python installations.
- **Ubuntu / Debian:** Install Tk support with `sudo apt install python3-tk` for the Python version you use.

### VS Code interpreter

If VS Code uses the wrong Python installation:

1. Open the project folder in VS Code.
2. Open the Command Palette with **Cmd + Shift + P** (macOS) or **Ctrl + Shift + P** (Windows).
3. Select **Python: Select Interpreter**.
4. Choose the interpreter inside this project's `.venv`:
   - macOS / Linux: `.venv/bin/python`
   - Windows: `.venv\\Scripts\\python.exe`

Verify the selected interpreter:

```bash
python --version
python -c "import sys; print(sys.executable)"
```

The executable path should point to this project's `.venv` directory.

## How to play

1. Start the game and enter names for Player 1 and Player 2.
2. Choose whether **X** or **O** goes first.
3. Players take turns selecting an empty square.
4. The first player to place three marks in a horizontal, vertical, or diagonal line wins.
5. If all nine squares are filled without a winning line, the game ends in a draw.
6. Use **Undo** to take back the latest move, **Rematch** to play again, or **Menu** to change the setup.

## Project structure

```text
tic-tac-toe-gui/
├── main.py
├── game/
│   ├── __init__.py
│   ├── board.py       # Board state, legal moves, win/draw detection
│   ├── ui.py          # CustomTkinter interface and game animations
│   ├── sounds.py      # Generated applause and sound playback
│   └── storage.py     # Local scoreboard and match history
├── tests/
│   └── test_board.py  # Unit tests for game rules
├── assets/            # Optional screenshots and media
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Run tests

Install the dependencies, then run:

```bash
python -m pytest -q
```

## Saved game data

After a completed match, the game creates `scores.json` in the project root. It stores the lifetime wins for X and O, draw count, and recent match results. The file is local to your machine and should remain untracked by Git.

## Technologies

- **Python** — game logic and application code
- **CustomTkinter** — desktop graphical interface
- **Tkinter Canvas** — confetti and winning-line animations
- **pytest** — automated tests

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
