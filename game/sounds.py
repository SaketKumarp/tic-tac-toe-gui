"""Cross-platform sound effects for the Tic Tac Toe game."""

from __future__ import annotations

import platform
import subprocess


def play_sound(root, enabled: bool = True, kind: str = "move") -> None:
    """Play a short platform-native sound without blocking the game UI."""
    if not enabled:
        return

    try:
        system = platform.system()
        if system == "Windows":
            import winsound

            alias = "SystemAsterisk" if kind == "win" else "SystemExclamation"
            winsound.PlaySound(alias, winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif system == "Darwin":
            sound_name = "Hero" if kind == "win" else "Glass" if kind == "draw" else "Tink"
            sound_path = "/System/Library/Sounds/" + sound_name + ".aiff"
            subprocess.Popen(["afplay", sound_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            root.bell()
    except Exception:
        try:
            root.bell()
        except Exception:
            pass
