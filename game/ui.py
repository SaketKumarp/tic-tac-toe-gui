"""Tkinter user interface with welcome, game, result and stats screens."""

import tkinter as tk
from tkinter import messagebox

from game.logic import TicTacToeGame
from game.storage import ScoreStorage
from game.sound import SoundEffects


class TicTacToeApp:
    BG = "#101820"
    PANEL = "#1b2935"
    PANEL_LIGHT = "#243746"
    TEXT = "#f4f7fa"
    MUTED = "#9fb0bd"
    ACCENT = "#36c98f"
    X_COLOR = "#61a8ff"
    O_COLOR = "#ffbd59"
    DANGER = "#ff7373"

    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe | Two Player")
        self.root.geometry("760x790")
        self.root.minsize(650, 700)
        self.root.configure(bg=self.BG)

        self.storage = ScoreStorage()
        self.sound = SoundEffects(fallback=self.root.bell)
        self.game = TicTacToeGame()
        self.player_x = ""
        self.player_o = ""
        self.cells = []
        self.screen = None

        self.show_welcome()
        self.sound.play('enter')

    def _clear_screen(self):
        if self.screen:
            self.screen.destroy()
        self.screen = tk.Frame(self.root, bg=self.BG)
        self.screen.pack(fill="both", expand=True, padx=34, pady=26)

    def _label(self, parent, text, size=12, color=None, bold=False, **kwargs):
        return tk.Label(
            parent,
            text=text,
            font=("Helvetica", size, "bold" if bold else "normal"),
            bg=kwargs.pop("bg", self.BG),
            fg=color or self.TEXT,
            **kwargs,
        )

    def _button(self, parent, text, command, color=None, width=18):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Helvetica", 12, "bold"),
            bg=color or self.ACCENT,
            fg=self.BG,
            activebackground=self.TEXT,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            padx=16,
            pady=12,
            width=width,
            cursor="hand2",
        )

    def _heading(self, parent, title, subtitle):
        self._label(parent, title, 30, self.TEXT, True).pack(pady=(8, 5))
        self._label(parent, subtitle, 11, self.MUTED).pack(pady=(0, 22))

    def show_welcome(self):
        self._clear_screen()
        self._heading(self.screen, "TIC TAC TOE", "THE CLASSIC TWO-PLAYER BATTLE")

        form = tk.Frame(self.screen, bg=self.PANEL, padx=28, pady=25)
        form.pack(fill="x", padx=45, pady=8)

        self._label(form, "PLAYER SETUP", 14, self.ACCENT, True, bg=self.PANEL).pack(anchor="w", pady=(0, 18))

        self._label(form, "PLAYER 1  ·  X", 10, self.X_COLOR, True, bg=self.PANEL).pack(anchor="w")
        self.name_x = tk.Entry(
            form, font=("Helvetica", 14), bg=self.PANEL_LIGHT, fg=self.TEXT,
            insertbackground=self.TEXT, relief="flat"
        )
        self.name_x.pack(fill="x", ipady=11, pady=(7, 18))
        self.name_x.insert(0, "Player 1")

        self._label(form, "PLAYER 2  ·  O", 10, self.O_COLOR, True, bg=self.PANEL).pack(anchor="w")
        self.name_o = tk.Entry(
            form, font=("Helvetica", 14), bg=self.PANEL_LIGHT, fg=self.TEXT,
            insertbackground=self.TEXT, relief="flat"
        )
        self.name_o.pack(fill="x", ipady=11, pady=(7, 8))
        self.name_o.insert(0, "Player 2")

        self._button(self.screen, "START GAME", self.start_game, width=22).pack(pady=(22, 10))
        self._button(self.screen, "LEADERBOARD & HISTORY", self.show_stats, self.PANEL_LIGHT, width=22).pack()

        self._label(
            self.screen,
            "Local multiplayer  •  Scores saved automatically",
            10, self.MUTED
        ).pack(side="bottom", pady=12)

    def start_game(self):
        name_x = self.name_x.get().strip()
        name_o = self.name_o.get().strip()

        if not name_x or not name_o:
            messagebox.showwarning("Names required", "Enter names for both players.")
            return
        if name_x.casefold() == name_o.casefold():
            messagebox.showwarning("Different names", "Please enter two different player names.")
            return

        self.player_x, self.player_o = name_x[:24], name_o[:24]
        self.game.reset()
        self.show_game()

    def show_game(self):
        self.sound.play('start')
        self._clear_screen()
        self._label(self.screen, "MATCH IN PROGRESS", 11, self.ACCENT, True).pack(pady=(0, 12))

        players = tk.Frame(self.screen, bg=self.BG)
        players.pack(fill="x", pady=(0, 15))
        self._player_card(players, self.player_x, "X", self.X_COLOR).pack(side="left", expand=True, fill="x", padx=(0, 7))
        self._player_card(players, self.player_o, "O", self.O_COLOR).pack(side="left", expand=True, fill="x", padx=(7, 0))

        self.turn_label = self._label(self.screen, "", 16, self.TEXT, True)
        self.turn_label.pack(pady=12)

        board_frame = tk.Frame(self.screen, bg=self.BG)
        board_frame.pack(pady=8)

        self.cells = []
        for position in range(9):
            cell = tk.Button(
                board_frame,
                text="",
                font=("Helvetica", 34, "bold"),
                width=4,
                height=2,
                bg=self.PANEL,
                fg=self.TEXT,
                activebackground=self.PANEL_LIGHT,
                activeforeground=self.TEXT,
                disabledforeground=self.TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda p=position: self.make_move(p),
            )
            cell.grid(row=position // 3, column=position % 3, padx=6, pady=6)
            self.cells.append(cell)

        self._button(self.screen, "BACK TO HOME", self.show_welcome, self.PANEL_LIGHT).pack(pady=18)
        self._update_turn()

    def _player_card(self, parent, name, symbol, color):
        card = tk.Frame(parent, bg=self.PANEL, padx=14, pady=14)
        self._label(card, symbol, 25, color, True, bg=self.PANEL).pack()
        self._label(card, name, 12, self.TEXT, True, bg=self.PANEL).pack(pady=(4, 0))
        self._label(card, f"{self.storage.data['players'].get(name, {}).get('wins', 0)} career wins", 9, self.MUTED, bg=self.PANEL).pack(pady=(4, 0))
        return card

    def _update_turn(self):
        if self.game.current_player == "X":
            name, color = self.player_x, self.X_COLOR
        else:
            name, color = self.player_o, self.O_COLOR
        self.turn_label.config(text=f"{name}'s turn  ·  {self.game.current_player}", fg=color)

    def make_move(self, position):
        mark = self.game.current_player
        result = self.game.play(position)
        if result == "invalid":
            return

        color = self.X_COLOR if mark == "X" else self.O_COLOR
        self.cells[position].config(text=mark, fg=color, state="disabled")

        if result in ("win", "draw"):
            self.storage.record_match(self.player_x, self.player_o, self.game.winner or "draw")
            self.show_result(result)
        else:
            self._update_turn()

    def show_result(self, result):
        self.sound.play('win' if result == 'win' else 'draw')
        self._clear_screen()

        if result == "win":
            winner_name = self.player_x if self.game.winner == "X" else self.player_o
            winner_color = self.X_COLOR if self.game.winner == "X" else self.O_COLOR
            self._label(self.screen, "MATCH COMPLETE", 11, self.ACCENT, True).pack(pady=(22, 12))
            self._label(self.screen, "🏆", 58, winner_color).pack(pady=5)
            self._label(self.screen, f"{winner_name} WINS!", 28, winner_color, True).pack(pady=8)
            self._label(self.screen, "Brilliant game. The victory has been saved.", 12, self.MUTED).pack(pady=4)
        else:
            self._label(self.screen, "MATCH COMPLETE", 11, self.ACCENT, True).pack(pady=(22, 12))
            self._label(self.screen, "🤝", 58, self.O_COLOR).pack(pady=5)
            self._label(self.screen, "IT'S A DRAW!", 28, self.TEXT, True).pack(pady=8)
            self._label(self.screen, "Well played by both players.", 12, self.MUTED).pack(pady=4)

        self._show_match_summary(self.screen)
        self._button(self.screen, "PLAY AGAIN", self.play_again, width=22).pack(pady=(28, 10))
        self._button(self.screen, "LEADERBOARD", self.show_stats, self.PANEL_LIGHT, width=22).pack(pady=5)
        self._button(self.screen, "MAIN MENU", self.show_welcome, self.PANEL_LIGHT, width=22).pack(pady=5)

    def _show_match_summary(self, parent):
        summary = tk.Frame(parent, bg=self.PANEL, padx=22, pady=18)
        summary.pack(fill="x", padx=55, pady=24)
        self._label(summary, f"{self.player_x}  ·  X", 12, self.X_COLOR, True, bg=self.PANEL).pack(pady=4)
        self._label(summary, "VS", 9, self.MUTED, True, bg=self.PANEL).pack()
        self._label(summary, f"{self.player_o}  ·  O", 12, self.O_COLOR, True, bg=self.PANEL).pack(pady=4)

    def play_again(self):
        self.game.reset()
        self.show_game()

    def show_stats(self):
        self._clear_screen()
        self._heading(self.screen, "LEADERBOARD", "ALL-TIME PLAYER STATISTICS")

        stats = self.storage.leaderboard()
        if not stats:
            self._label(self.screen, "No matches played yet.", 13, self.MUTED).pack(pady=25)
        else:
            header = tk.Frame(self.screen, bg=self.PANEL_LIGHT, padx=12, pady=10)
            header.pack(fill="x", padx=10, pady=(0, 4))
            for text, width in (("PLAYER", 20), ("WINS", 8), ("GAMES", 8), ("DRAWS", 8)):
                self._label(header, text, 9, self.MUTED, True, bg=self.PANEL_LIGHT, width=width, anchor="w").pack(side="left")

            for rank, (name, record) in enumerate(stats, start=1):
                row = tk.Frame(self.screen, bg=self.PANEL, padx=12, pady=10)
                row.pack(fill="x", padx=10, pady=3)
                self._label(row, f"{rank}. {name}", 10, self.TEXT, True, bg=self.PANEL, width=20, anchor="w").pack(side="left")
                for key in ("wins", "games", "draws"):
                    self._label(row, str(record[key]), 10, self.ACCENT, True, bg=self.PANEL, width=8, anchor="w").pack(side="left")

        self._label(self.screen, "RECENT MATCHES", 11, self.ACCENT, True).pack(anchor="w", padx=12, pady=(22, 8))
        matches = self.storage.recent_matches()
        if not matches:
            self._label(self.screen, "Your match history will appear here.", 10, self.MUTED).pack()
        else:
            for match in matches:
                if match["result"] == "draw":
                    result_text = "Draw"
                elif match["result"] == "X":
                    result_text = f"{match['player_x']} won"
                else:
                    result_text = f"{match['player_o']} won"
                line = f"{match['player_x']} vs {match['player_o']}  —  {result_text}"
                self._label(self.screen, line, 10, self.TEXT).pack(anchor="w", padx=18, pady=3)

        self._button(self.screen, "BACK TO HOME", self.show_welcome, self.PANEL_LIGHT).pack(pady=24)
