"""Small cross-platform sound effects using only Python's standard library."""

import math
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
from pathlib import Path


class SoundEffects:
    """Generate short tones and play them without blocking the Tkinter UI."""

    NOTES = {
        "enter": [(523, 0.12), (659, 0.12), (784, 0.20)],
        "start": [(392, 0.12), (523, 0.12), (659, 0.18)],
        "win": [(523, 0.12), (659, 0.12), (784, 0.12), (1047, 0.28)],
        "draw": [(440, 0.18), (392, 0.24)],
    }

    def __init__(self, fallback=None):
        self.fallback = fallback
        self.sound_dir = Path(tempfile.gettempdir()) / "tic_tac_toe_sounds"
        self.sound_dir.mkdir(exist_ok=True)
        self.files = {}

        for name, notes in self.NOTES.items():
            path = self.sound_dir / f"{name}.wav"
            if not path.exists():
                self._create_tone(path, notes)
            self.files[name] = path

    @staticmethod
    def _create_tone(path, notes):
        sample_rate = 44100
        frames = bytearray()

        for frequency, duration in notes:
            count = int(sample_rate * duration)
            for index in range(count):
                edge = min(1.0, index / 250, (count - index) / 400)
                sample = int(11000 * edge * math.sin(2 * math.pi * frequency * index / sample_rate))
                frames.extend(struct.pack("<h", sample))

        with wave.open(str(path), "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(sample_rate)
            audio.writeframes(frames)

    def play(self, event):
        path = self.files.get(event)
        if path is None:
            return

        try:
            if sys.platform == "win32":
                import winsound
                winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif sys.platform == "darwin":
                subprocess.Popen(["afplay", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                player = shutil.which("paplay") or shutil.which("aplay")
                if player:
                    subprocess.Popen([player, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                elif self.fallback:
                    self.fallback()
        except (OSError, RuntimeError):
            if self.fallback:
                self.fallback()
