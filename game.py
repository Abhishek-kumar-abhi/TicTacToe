import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import json
import math
import os

class TicTacToeApp(tk.Tk):
    """Main application class that manages frames and shared data."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Tic-Tac-Toe")
        self.geometry("500x600")
        self.configure(bg="#1a1a2e")

        # --- Fonts ---
        self.title_font = tkfont.Font(family='Helvetica', size=24, weight="bold")
        self.button_font = tkfont.Font(family='Helvetica', size=14)
        self.info_font = tkfont.Font(family='Helvetica', size=12)

        # --- File Path for Records ---
        # This makes the records file relative to the script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.records_path = os.path.join(script_dir, "records.json")

        # --- Shared Data ---
        self.game_mode = tk.StringVar(value="2P")  # "2P" or "1P"
        self.records = self.load_records()

        # --- Frame Container ---
        container = tk.Frame(self, bg="#1a1a2e")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomeFrame, SettingsFrame, GameFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeFrame")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, page_name):
        """Raises a specific frame to the top."""
        frame = self.frames[page_name]
        # Special action for frames that need updates when shown
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

    def load_records(self):
        """Loads records from records.json, creating it if it doesn't exist."""
        try:
            with open(self.records_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is empty, create a default structure
            default_records = {"player_x_wins": 0, "player_o_wins": 0, "draws": 0}
            self.save_records(default_records) # Save it immediately
            return default_records

    def save_records(self, data=None):
        """Saves the current records to records.json."""
        if data is None:
            data = self.records
        with open(self.records_path, "w") as f:
            json.dump(data, f, indent=4)

    def on_closing(self):
        """Handles the application closing event."""
        self.save_records()
        self.destroy()

class GradientCanvas(tk.Canvas):
    """A canvas that draws a gradient background."""
    def __init__(self, parent, color1, color2, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = (r2 - r1) / height
        g_ratio = (g2 - g1) / height
        b_ratio = (b2 - b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr:04x}{ng:04x}{nb:04x}'
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.lower("gradient")

class WelcomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        canvas = GradientCanvas(self, "#1f4068", "#162447")
        canvas.pack(fill="both", expand=True)

        title = tk.Label(canvas, text="Tic-Tac-Toe", font=controller.title_font, bg="#1f4068", fg="#e0fbfc")
        title.place(relx=0.5, rely=0.2, anchor="center")

        play_button = tk.Button(canvas, text="Play Game", font=controller.button_font, bg="#61dafb", fg="#1a1a2e", relief="flat", padx=20, pady=10, command=lambda: controller.show_frame("GameFrame"))
        play_button.place(relx=0.5, rely=0.4, anchor="center")

        settings_button = tk.Button(canvas, text="Settings & Records", font=controller.button_font, bg="#ffc107", fg="#1a1a2e", relief="flat", padx=20, pady=10, command=lambda: controller.show_frame("SettingsFrame"))
        settings_button.place(relx=0.5, rely=0.55, anchor="center")

        quit_button = tk.Button(canvas, text="Quit", font=controller.button_font, bg="#ff5722", fg="white", relief="flat", padx=20, pady=10, command=controller.on_closing)
        quit_button.place(relx=0.5, rely=0.7, anchor="center")

class SettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        canvas = GradientCanvas(self, "#1f4068", "#162447")
        canvas.pack(fill="both", expand=True)

        title = tk.Label(canvas, text="Settings & Records", font=controller.title_font, bg="#1f4068", fg="#e0fbfc")
        title.place(relx=0.5, rely=0.1, anchor="center")

        # Game Mode
        mode_label = tk.Label(canvas, text="Game Mode", font=controller.button_font, bg="#162447", fg="white")
        mode_label.place(relx=0.5, rely=0.25, anchor="center")
        
        r1 = tk.Radiobutton(canvas, text="Player vs Player", variable=controller.game_mode, value="2P", font=controller.info_font, bg="#162447", fg="#e0fbfc", selectcolor="#1a1a2e", activebackground="#162447", activeforeground="#e0fbfc", highlightthickness=0)
        r1.place(relx=0.5, rely=0.32, anchor="center")
        r2 = tk.Radiobutton(canvas, text="Player vs AI", variable=controller.game_mode, value="1P", font=controller.info_font, bg="#162447", fg="#e0fbfc", selectcolor="#1a1a2e", activebackground="#162447", activeforeground="#e0fbfc", highlightthickness=0)
        r2.place(relx=0.5, rely=0.38, anchor="center")

        # Records
        records_label = tk.Label(canvas, text="Records", font=controller.button_font, bg="#162447", fg="white")
        records_label.place(relx=0.5, rely=0.5, anchor="center")

        self.records_var = tk.StringVar()
        records_display = tk.Label(canvas, textvariable=self.records_var, font=controller.info_font, bg="#1a1a2e", fg="#61dafb", justify="left", padx=20, pady=10)
        records_display.place(relx=0.5, rely=0.65, anchor="center")

        back_button = tk.Button(canvas, text="Back to Menu", font=controller.button_font, bg="#607D8B", fg="white", relief="flat", padx=20, pady=10, command=lambda: controller.show_frame("WelcomeFrame"))
        back_button.place(relx=0.5, rely=0.85, anchor="center")

    def on_show(self):
        """Update the records display when the frame is shown."""
        rec = self.controller.records
        self.records_var.set(f"Player X Wins: {rec['player_x_wins']}\nPlayer O Wins: {rec['player_o_wins']}\nDraws: {rec['draws']}")

class GameFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.board_size = 300
        self.cell_size = self.board_size / 3

        canvas = GradientCanvas(self, "#1f4068", "#162447")
        canvas.pack(fill="both", expand=True)

        self.info_label = tk.Label(canvas, text="", font=controller.button_font, bg="#1f4068", fg="white")
        self.info_label.place(relx=0.5, rely=0.1, anchor="center")

        self.board_canvas = tk.Canvas(canvas, width=self.board_size, height=self.board_size, bg="#1a1a2e", highlightthickness=0)
        self.board_canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.board_canvas.bind("<Button-1>", self.on_board_click)

        menu_button = tk.Button(canvas, text="Main Menu", font=controller.button_font, bg="#607D8B", fg="white", relief="flat", padx=20, pady=10, command=lambda: controller.show_frame("WelcomeFrame"))
        menu_button.place(relx=0.5, rely=0.9, anchor="center")

    def on_show(self):
        """Called when the frame is raised."""
        self.start_new_game()

    def start_new_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.info_label.config(text=f"Player {self.current_player}'s Turn")
        self.draw_board()

    def draw_board(self):
        self.board_canvas.delete("all")
        for i in range(1, 3):
            self.board_canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.board_size, fill="#61dafb", width=4)
            self.board_canvas.create_line(0, i * self.cell_size, self.board_size, i * self.cell_size, fill="#61dafb", width=4)

    def on_board_click(self, event):
        if self.game_over: return
        col = int(event.x // self.cell_size)
        row = int(event.y // self.cell_size)

        if self.board[row][col] == "":
            self.make_move(row, col, self.current_player)
            if not self.game_over and self.controller.game_mode.get() == "1P" and self.current_player == "O":
                self.after(500, self.ai_move)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.draw_symbol(row, col, player)

        if self.check_winner(player):
            self.end_game(winner=player)
        elif self.check_draw():
            self.end_game(winner="Draw")
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.info_label.config(text=f"Player {self.current_player}'s Turn")

    def draw_symbol(self, row, col, player):
        x = col * self.cell_size + self.cell_size / 2
        y = row * self.cell_size + self.cell_size / 2
        half = self.cell_size / 2 - 15
        if player == "X":
            self.board_canvas.create_line(x - half, y - half, x + half, y + half, fill="#ffc107", width=5)
            self.board_canvas.create_line(x - half, y + half, x + half, y - half, fill="#ffc107", width=5)
        else:
            self.board_canvas.create_oval(x - half, y - half, x + half, y + half, outline="#ff5722", width=5)

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)): return True
            if all(self.board[j][i] == player for j in range(3)): return True
        if all(self.board[i][i] == player for i in range(3)): return True
        if all(self.board[i][2 - i] == player for i in range(3)): return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def end_game(self, winner):
        self.game_over = True
        if winner == "Draw":
            message = "It's a Draw!"
            self.controller.records["draws"] += 1
        else:
            message = f"Player {winner} wins!"
            if winner == 'X': self.controller.records["player_x_wins"] += 1
            else: self.controller.records["player_o_wins"] += 1
        
        self.info_label.config(text=message)
        self.controller.save_records()
        messagebox.showinfo("Game Over", message, parent=self)

    def ai_move(self):
        if self.game_over: return
        best_score = -math.inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            self.make_move(best_move[0], best_move[1], "O")

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner("O"): return 1
        if self.check_winner("X"): return -1
        if self.check_draw(): return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "O"
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "X"
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

if __name__ == "__main__":
    app = TicTacToeApp()
    app.mainloop()