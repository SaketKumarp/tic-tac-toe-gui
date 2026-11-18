# Tic Tac Toe — Two Player Edition

A two-player desktop Tic-Tac-Toe game built with Python and Tkinter.

## Features

- Welcome screen with names for both players
- Separate game and match-result screens
- Alternating X and O turns with occupied-cell protection
- Win and draw detection
- Persistent player statistics and recent match history
- Leaderboard ordered by wins
- New match and return-to-menu actions
- Welcome, match-start, win and draw sound effects (generated locally; no audio downloads)

## Requirements

- Python 3.9+
- Tkinter (included with most standard Python installations)
- No third-party packages

## Run

From the project root:

```bash
python main.py
```

On macOS, if you use the project's virtual environment:

```bash
source .venv/bin/activate
python main.py
```

## Storage

The game creates `scores.json` in the project root after the first completed match. It stores player games, wins, draws and the most recent 100 match records. Keep this file if you want to preserve statistics.

## Project structure

```text
tic-tac-toe-gui/
├── main.py
├── game/
│   ├── __init__.py
│   ├── logic.py
│   ├── storage.py
│   ├── sound.py
│   └── ui.py
├── scores.json       # created automatically
├── requirements.txt
└── README.md
```

## Concepts demonstrated

Tkinter frames and widgets, grid layout, event callbacks, classes, lists, loops, conditionals, JSON file handling, and separation of UI, game logic and storage.
