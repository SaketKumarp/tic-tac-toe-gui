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

## Game flow diagram

The application is event-driven: Tkinter's `mainloop()` waits for user actions, and button callbacks handle each move.

```mermaid
flowchart TD
    A([Start]) --> B[main.py: create Tk root]
    B --> C[Create TicTacToeApp]
    C --> D[Initialize game, storage and sound]
    D --> E[Show welcome screen]
    E --> F{User selects an action}
    F -->|Start Game| G[Read and validate player names]
    G --> H{Names valid and different?}
    H -->|No| I[Show validation message]
    I --> E
    H -->|Yes| J[Reset board and set current player to X]
    J --> K[Show game screen and create 9 buttons]
    K --> L[Wait for a cell click]
    L --> M[make_move(position)]
    M --> N[game.play(position)]
    N --> O{Move valid?}
    O -->|No| L
    O -->|Yes| P[Place current player's mark]
    P --> Q{Winning combination found?}
    Q -->|Yes| R[Set winner and finish game]
    Q -->|No| S{Board full?}
    S -->|Yes| T[Finish game as a draw]
    S -->|No| U[Switch X/O turn and update turn label]
    U --> L
    R --> V[Save match statistics]
    T --> V
    V --> W[Show result screen and play result sound]
    W --> X{User selects an action}
    X -->|Play Again| J
    X -->|Leaderboard / History| Y[Show saved statistics]
    Y --> Z[Return to welcome screen]
    X -->|Main Menu| Z
    F -->|Leaderboard / History| Y
```

## Concepts demonstrated

Tkinter frames and widgets, grid layout, event callbacks, classes, lists, loops, conditionals, JSON file handling, and separation of UI, game logic and storage.
