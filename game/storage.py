"""Persistent scoreboard and recent game history stored as JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent.parent / "scores.json"
DEFAULT_DATA: dict[str, Any] = {
    "scores": {"X": 0, "O": 0, "Draw": 0},
    "history": [],
}


def load_data(path: Path = DATA_FILE) -> dict[str, Any]:
    """Load saved scores, falling back safely when the file is missing or invalid."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        scores = data.get("scores", {})
        history = data.get("history", [])
        return {
            "scores": {key: int(scores.get(key, 0)) for key in ("X", "O", "Draw")},
            "history": history if isinstance(history, list) else [],
        }
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return {"scores": DEFAULT_DATA["scores"].copy(), "history": []}


def save_data(data: dict[str, Any], path: Path = DATA_FILE) -> None:
    """Write data atomically so an interrupted save does not corrupt the file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temporary.replace(path)


def record_result(result: str, player_names: dict[str, str], mode: str,
                  path: Path = DATA_FILE) -> dict[str, Any]:
    """Increment the scoreboard and append a compact record of the finished game."""
    data = load_data(path)
    key = result if result in ("X", "O") else "Draw"
    data["scores"][key] += 1
    data["history"].insert(0, {
        "result": key,
        "winner": player_names.get(key, key) if key != "Draw" else "Draw",
        "mode": mode,
    })
    data["history"] = data["history"][:50]
    save_data(data, path)
    return data
