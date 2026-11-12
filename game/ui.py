"""CustomTkinter interface for the Tic Tac Toe game."""

from __future__ import annotations

import random

import customtkinter as ctk
from tkinter import Canvas

from game.board import GameBoard, O, X
from game.sounds import play_sound
from game.storage import load_data, record_result

BG = "#10131c"
PANEL = "#191f2d"
ACCENT = "#7c5cff"
X_COLOR = "#ff6b6b"
O_COLOR = "#54c7ec"
WIN_COLOR = "#2ecc71"
TEXT = "#f4f6fb"
MUTED = "#aab2c5"


class TicTacToeApp(ctk.CTk):
    """Own the two-player application screens and coordinate board and storage."""

    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Tic Tac Toe | Python GUI")
        self.geometry("560x720")
        self.minsize(480, 650)
        self.configure(fg_color=BG)
        self.board = GameBoard()
        self.saved_data = load_data()
        self.names = {X: "Player 1", O: "Player 2"}
        self.sound_enabled = True
        self.buttons: list[ctk.CTkButton] = []
        self.game_frame = None
        self.menu_frame = None
        self.win_canvas = None
        self.after_id = None
        self._show_menu()

    def _clear_screen(self) -> None:
        if getattr(self, "confetti_after_id", None):
            try:
                self.after_cancel(self.confetti_after_id)
            except Exception:
                pass
            self.confetti_after_id = None
        for child in self.winfo_children():
            child.destroy()
        self.buttons = []
        self.win_canvas = None

    def _show_menu(self) -> None:
        self._clear_screen()
        frame = ctk.CTkFrame(self, fg_color=BG)
        frame.pack(fill="both", expand=True, padx=28, pady=24)
        ctk.CTkLabel(frame, text="TIC TAC TOE", font=("Helvetica", 34, "bold"),
                     text_color=TEXT).pack(pady=(28, 4))
        ctk.CTkLabel(frame, text="A little strategy goes a long way.",
                     font=("Helvetica", 14), text_color=MUTED).pack(pady=(0, 22))

        ctk.CTkLabel(frame, text="PLAYER NAMES", text_color=MUTED,
                     font=("Helvetica", 12, "bold")).pack(anchor="w", padx=18)
        names_frame = ctk.CTkFrame(frame, fg_color="transparent")
        names_frame.pack(fill="x", padx=18, pady=6)
        self.x_name_entry = ctk.CTkEntry(names_frame, placeholder_text="Player X name")
        self.x_name_entry.insert(0, "Player 1")
        self.x_name_entry.pack(side="left", expand=True, fill="x", padx=(0, 6))
        self.o_name_entry = ctk.CTkEntry(names_frame, placeholder_text="Player 2 (O)")
        self.o_name_entry.insert(0, "Player 2")
        self.o_name_entry.pack(side="left", expand=True, fill="x", padx=(6, 0))

        settings = ctk.CTkFrame(frame, fg_color=PANEL, corner_radius=14)
        settings.pack(fill="x", padx=18, pady=14)
        ctk.CTkLabel(settings, text="GAME SETTINGS", text_color=MUTED,
                     font=("Helvetica", 12, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
        self.first_var = ctk.StringVar(value="X")
        row = ctk.CTkFrame(settings, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(row, text="First turn", text_color=TEXT).pack(side="left")
        ctk.CTkSegmentedButton(row, values=["X", "O"], variable=self.first_var).pack(side="right")

        self.sound_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(frame, text="Sound effects", variable=self.sound_var,
                        text_color=TEXT, fg_color=ACCENT, hover_color=ACCENT).pack(anchor="w", padx=18, pady=4)
        ctk.CTkButton(frame, text="START GAME", height=48, corner_radius=12,
                      fg_color=ACCENT, hover_color="#6748df", font=("Helvetica", 16, "bold"),
                      command=self._start_game).pack(fill="x", padx=18, pady=(16, 10))
        scores = self.saved_data["scores"]
        ctk.CTkLabel(frame, text=f"Lifetime score  ·  X {scores['X']}     O {scores['O']}     Draws {scores['Draw']}",
                     text_color=MUTED, font=("Helvetica", 12)).pack(pady=8)

    def _start_game(self) -> None:
        self.sound_enabled = self.sound_var.get()
        x_name = self.x_name_entry.get().strip() or "Player 1"
        o_name = self.o_name_entry.get().strip() or "Player 2"
        self.names = {X: x_name, O: o_name}
        self._build_game_screen(self.first_var.get())

    def _build_game_screen(self, starting_player: str) -> None:
        self._clear_screen()
        self.board.reset(starting_player)
        frame = ctk.CTkFrame(self, fg_color=BG)
        frame.pack(fill="both", expand=True, padx=24, pady=22)
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x")
        ctk.CTkButton(top, text="← Menu", width=90, fg_color=PANEL,
                      hover_color="#293247", command=self._show_menu).pack(side="left")
        ctk.CTkLabel(top, text="TIC TAC TOE", font=("Helvetica", 22, "bold"),
                     text_color=TEXT).pack(side="right")

        self.status_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 19, "bold"), text_color=TEXT)
        self.status_label.pack(pady=(30, 8))
        self.result_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 14), text_color=WIN_COLOR)
        self.result_label.pack(pady=(0, 10))
        self.celebration_canvas = Canvas(frame, width=500, height=96, bg=BG,
                                         highlightthickness=0, bd=0)
        self.celebration_canvas.pack_forget()
        self.confetti_particles: list[dict] = []
        self.confetti_after_id = None
        self.score_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 13), text_color=MUTED)
        self.score_label.pack(pady=(0, 20))

        self.grid_frame = ctk.CTkFrame(frame, fg_color=PANEL, corner_radius=18)
        self.grid_frame.pack(pady=8)
        for index in range(9):
            button = ctk.CTkButton(
                self.grid_frame, text="", width=105, height=105, corner_radius=12,
                fg_color="#252d40", hover_color="#35415b", text_color=TEXT,
                font=("Helvetica", 42, "bold"), command=lambda i=index: self._on_cell_click(i),
            )
            button.grid(row=index // 3, column=index % 3, padx=5, pady=5)
            button.bind("<Enter>", lambda event, i=index: self._hover_cell(i, True))
            button.bind("<Leave>", lambda event, i=index: self._hover_cell(i, False))
            self.buttons.append(button)

        controls = ctk.CTkFrame(frame, fg_color="transparent")
        controls.pack(fill="x", pady=22)
        ctk.CTkButton(controls, text="Undo", command=self._undo, fg_color=PANEL,
                      hover_color="#293247").pack(side="left", expand=True, padx=4)
        ctk.CTkButton(controls, text="Rematch", command=lambda: self._build_game_screen(self.first_var.get()),
                      fg_color=ACCENT, hover_color="#6748df").pack(side="left", expand=True, padx=4)
        ctk.CTkButton(controls, text="New Setup", command=self._show_menu, fg_color=PANEL,
                      hover_color="#293247").pack(side="left", expand=True, padx=4)
        self._update_labels()

    def _hover_cell(self, index: int, entered: bool) -> None:
        if self.board.is_over or self.board.cells[index]:
            return
        self.buttons[index].configure(fg_color="#3b4661" if entered else "#252d40")

    def _on_cell_click(self, index: int) -> None:
        if self.board.is_over or self.board.cells[index]:
            return
        self._play_move(index)

    def _play_move(self, index: int) -> None:
        player = self.board.current_player
        if not self.board.make_move(index):
            return
        color = X_COLOR if player == X else O_COLOR
        self.buttons[index].configure(text=player, text_color=color, fg_color="#30394d", hover=False)
        play_sound(self, self.sound_enabled)
        self._update_labels()
        if self.board.winner:
            self._finish_game(self.board.winner)
        elif self.board.is_draw:
            self._finish_game("Draw")

    def _finish_game(self, result: str) -> None:
        if result == "Draw":
            self.result_label.configure(
                text="🤝  IT'S A DRAW!  GOOD GAME!",
                text_color="#f6c85f",
                font=("Helvetica", 17, "bold"),
            )
            play_sound(self, self.sound_enabled, kind="draw")
        else:
            winner_name = self.names[result]
            self.result_label.configure(
                text=f"🏆  {winner_name} ({result}) IS THE CHAMPION!  🎉",
                text_color="#ffd166",
                font=("Helvetica", 17, "bold"),
            )
            for index in self.board.winning_combo or ():
                self.buttons[index].configure(text_color="#ffd166", fg_color="#3b3040")
            self._start_confetti()
            self._animate_winning_line()
            self._pulse_winner_banner(0)
            play_sound(self, self.sound_enabled, kind="win")

        self.saved_data = record_result(result, self.names, "PvP")
        self._update_labels()
        for button in self.buttons:
            button.configure(hover=False)

    def _pulse_winner_banner(self, step: int) -> None:
        """Give the winner banner a brief celebratory glow pulse."""
        if not self.result_label.winfo_exists() or step >= 8:
            return
        colors = ["#ffd166", "#fff3bf", "#ffb703", "#fff3bf"]
        self.result_label.configure(
            text_color=colors[step % len(colors)],
            font=("Helvetica", 17 if step % 2 else 19, "bold"),
        )
        self.after(180, lambda: self._pulse_winner_banner(step + 1))

    def _start_confetti(self) -> None:
        """Show a short burst of falling confetti below the result message."""
        canvas = self.celebration_canvas
        canvas.pack(fill="x", pady=(0, 4), before=self.score_label)
        canvas.delete("all")
        colors = ["#ffd166", "#06d6a0", "#7c5cff", "#54c7ec", "#ff6b6b", "#ffffff"]
        self.confetti_particles = [
            {
                "x": random.randint(8, 492),
                "y": random.uniform(20, 96),
                "vx": random.uniform(-3.4, 3.4),
                "vy": random.uniform(-6.5, -1.0),
                "size": random.randint(4, 9),
                "color": random.choice(colors),
                "rotation": random.uniform(0, 6.28),
            }
            for _ in range(65)
        ]
        self._animate_confetti(0)

    def _animate_confetti(self, frame: int) -> None:
        """Animate a colorful burst of confetti and firework-like sparkles."""
        if not self.winfo_exists() or not self.celebration_canvas.winfo_exists():
            return

        canvas = self.celebration_canvas
        canvas.delete("confetti")
        for particle in self.confetti_particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.16
            particle["rotation"] += 0.18

            x, y, size = particle["x"], particle["y"], particle["size"]
            # Tiny angled rectangles look like pieces of falling party confetti.
            dx = size * 0.65
            dy = size * 0.25
            canvas.create_polygon(
                x, y, x + dx, y + dy, x + dx * 0.65, y + size,
                x - dx * 0.3, y + size * 0.7,
                fill=particle["color"], outline="", tags="confetti",
            )

        if frame < 78 and self.board.winner:
            self.confetti_after_id = self.after(
                30, lambda: self._animate_confetti(frame + 1)
            )
        else:
            canvas.delete("confetti")
            canvas.pack_forget()
            self.confetti_after_id = None

    def _animate_winning_line(self) -> None:
        if not self.board.winning_combo:
            return
        if self.win_canvas:
            self.win_canvas.destroy()
        self.win_canvas = Canvas(self.grid_frame, width=330, height=330,
                                 bg=PANEL, highlightthickness=0, bd=0)
        self.win_canvas.place(x=0, y=0, width=330, height=330)
        combo = self.board.winning_combo
        first, last = combo[0], combo[-1]
        x1, y1 = 60 + (first % 3) * 110, 60 + (first // 3) * 110
        x2, y2 = 60 + (last % 3) * 110, 60 + (last // 3) * 110
        self._draw_line_step(x1, y1, x2, y2, 0)

    def _draw_line_step(self, x1: int, y1: int, x2: int, y2: int, step: int) -> None:
        if not self.win_canvas or not self.win_canvas.winfo_exists():
            return
        progress = min(step / 15, 1)
        self.win_canvas.delete("line")
        self.win_canvas.create_line(x1, y1, x1 + (x2 - x1) * progress,
                                    y1 + (y2 - y1) * progress,
                                    fill=WIN_COLOR, width=7, capstyle="round", tags="line")
        if progress < 1:
            self.after(18, lambda: self._draw_line_step(x1, y1, x2, y2, step + 1))

    def _undo(self) -> None:
        if not self.board.move_history or self.board.is_over:
            return
        index = self.board.undo_move()
        if index is not None:
            self.buttons[index].configure(text="", text_color=TEXT, fg_color="#252d40", hover=True)
        if self.win_canvas:
            self.win_canvas.destroy()
            self.win_canvas = None
        self.result_label.configure(text="")
        self._update_labels()

    def _update_labels(self) -> None:
        if not hasattr(self, "status_label") or not self.status_label.winfo_exists():
            return
        if self.board.is_over:
            self.status_label.configure(text="GAME OVER")
        else:
            player = self.board.current_player
            name = self.names[player]
            self.status_label.configure(text=f"{name}'s turn  ·  {player}")
        scores = self.saved_data["scores"]
        self.score_label.configure(text=f"X: {scores['X']}     O: {scores['O']}     Draws: {scores['Draw']}")
