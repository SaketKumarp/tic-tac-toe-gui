"""Cross-platform sound effects, including a generated applause effect."""

from __future__ import annotations

import math
import os
import platform
import random
import struct
import subprocess
import tempfile
import wave

_APPLAUSE_FILE: str | None = None


def _make_applause_file() -> str:
    """Synthesize a short crowd-applause sound from layered clap transients."""
    global _APPLAUSE_FILE
    if _APPLAUSE_FILE and os.path.exists(_APPLAUSE_FILE):
        return _APPLAUSE_FILE

    sample_rate = 22050
    duration = 2.4
    total = int(sample_rate * duration)
    samples = [0.0] * total
    rng = random.Random()

    # Each transient is a noisy, sharp clap with a fast attack and short decay.
    event_time = 0.0
    while event_time < duration:
        event_time += rng.uniform(0.025, 0.095)
        start = int(event_time * sample_rate)
        length = int(rng.uniform(0.035, 0.11) * sample_rate)
        amplitude = rng.uniform(0.25, 0.85)
        for offset in range(length):
            index = start + offset
            if index >= total:
                break
            t = offset / sample_rate
            envelope = math.exp(-t * rng.uniform(24.0, 42.0))
            noise = rng.uniform(-1.0, 1.0)
            # Add a little resonant body so it sounds more like hands clapping.
            body = math.sin(2 * math.pi * 950 * t) * 0.18
            samples[index] += amplitude * envelope * (noise * 0.82 + body)

    peak = max(max(samples), abs(min(samples)), 0.001)
    pcm = bytearray()
    for value in samples:
        clipped = max(-1.0, min(1.0, value / peak * 0.88))
        pcm.extend(struct.pack("<h", int(clipped * 32767)))

    handle = tempfile.NamedTemporaryFile(prefix="tic_tac_toe_applause_", suffix=".wav", delete=False)
    handle.close()
    with wave.open(handle.name, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(sample_rate)
        audio.writeframes(pcm)

    _APPLAUSE_FILE = handle.name
    return _APPLAUSE_FILE


def play_sound(root, enabled: bool = True, kind: str = "move") -> None:
    """Play a platform-native sound without blocking the game UI."""
    if not enabled:
        return

    try:
        system = platform.system()
        if kind == "win":
            applause_path = _make_applause_file()
            if system == "Windows":
                import winsound

                winsound.PlaySound(
                    applause_path,
                    winsound.SND_FILENAME | winsound.SND_ASYNC,
                )
            elif system == "Darwin":
                subprocess.Popen(
                    ["afplay", applause_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                subprocess.Popen(
                    ["aplay", applause_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            return

        if system == "Windows":
            import winsound

            alias = "SystemExclamation" if kind == "draw" else "SystemAsterisk"
            winsound.PlaySound(alias, winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif system == "Darwin":
            sound_name = "Glass" if kind == "draw" else "Tink"
            sound_path = "/System/Library/Sounds/" + sound_name + ".aiff"
            subprocess.Popen(
                ["afplay", sound_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            root.bell()
    except Exception:
        try:
            root.bell()
        except Exception:
            pass
