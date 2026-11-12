"""Small cross-platform sound helper using Tk's built-in bell."""

from __future__ import annotations


def play_sound(root, enabled: bool = True) -> None:
    """Play a short system notification sound when sound is enabled."""
    if enabled:
        try:
            root.bell()
        except Exception:
            # Audio is optional; gameplay should never depend on it.
            pass
