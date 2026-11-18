"""Persistent player statistics stored in a local JSON file."""

import json
from pathlib import Path
from datetime import datetime


class ScoreStorage:
    def __init__(self):
        self.file_path = Path(__file__).resolve().parent.parent / "scores.json"
        self.data = self._load()

    def _empty_data(self):
        return {"players": {}, "matches": []}

    def _load(self):
        if not self.file_path.exists():
            return self._empty_data()

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                return self._empty_data()
            data.setdefault("players", {})
            data.setdefault("matches", [])
            return data
        except (json.JSONDecodeError, OSError):
            return self._empty_data()

    def _save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.file_path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)
        temporary_path.replace(self.file_path)

    def _ensure_player(self, name):
        if name not in self.data["players"]:
            self.data["players"][name] = {
                "games": 0,
                "wins": 0,
                "draws": 0,
            }
        return self.data["players"][name]

    def record_match(self, player_x, player_o, result):
        """Record result as 'X', 'O', or 'draw'."""
        x_stats = self._ensure_player(player_x)
        o_stats = self._ensure_player(player_o)

        x_stats["games"] += 1
        o_stats["games"] += 1

        if result == "X":
            x_stats["wins"] += 1
        elif result == "O":
            o_stats["wins"] += 1
        else:
            x_stats["draws"] += 1
            o_stats["draws"] += 1

        self.data["matches"].append({
            "player_x": player_x,
            "player_o": player_o,
            "result": result,
            "played_at": datetime.now().isoformat(timespec="seconds"),
        })
        self.data["matches"] = self.data["matches"][-100:]
        self._save()

    def leaderboard(self):
        return sorted(
            self.data["players"].items(),
            key=lambda item: (item[1]["wins"], item[1]["games"]),
            reverse=True,
        )

    def recent_matches(self, limit=8):
        return list(reversed(self.data["matches"][-limit:]))
