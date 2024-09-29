import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

class PrecisionPathGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Precision Path")
        self.master.geometry("1000x800")
        self.master.configure(bg="#2C3E50")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=10, relief="flat", background="#3498DB")

        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame, width=980, height=700,
                                bg="#ECF0F1", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.path = self.create_path()
        self.start_x, self.start_y = self.path[0]
        self.end_x, self.end_y = self.path[-1]

        self.draw_path()
        self.create_buttons()

        self.canvas.bind("<Motion>", self.check_position)
        self.game_started = False
        self.game_over = False

        self.info_label = ttk.Label(self.frame, text="Click Start",
                                    font=("Arial", 12), background="#2C3E50", foreground="#ECF0F1")
        self.info_label.pack(pady=5)

    def create_path(self):
        path = [(50, 350)]
        current_x, current_y = path[0]

        while current_x < 930:
            direction = random.choice(['right', 'up', 'down'])
            if direction == 'right':
                new_x = min(current_x + random.randint(50, 150), 930)
                path.append((new_x, current_y))
                current_x = new_x
            elif direction == 'up':
                new_y = max(current_y - random.randint(50, 150), 50)
                path.append((current_x, new_y))
                current_y = new_y
            else:
                new_y = min(current_y + random.randint(50, 150), 650)
                path.append((current_x, new_y))
                current_y = new_y

        path.append((930, current_y))
        return path

    def draw_path(self):
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, width=30, fill="#3498DB",
                                    capstyle=tk.ROUND, joinstyle=tk.ROUND)

    def create_buttons(self):
        self.start_button = ttk.Button(self.canvas, text="Start", command=self.start_game)
        self.start_button.place(x=self.start_x - 30, y=self.start_y - 15)

        self.end_button = ttk.Button(self.canvas, text="End", command=self.end_game)
        self.end_button.place(x=self.end_x - 30, y=self.end_y - 15)

    def start_game(self):
        self.game_started = True
        self.start_button.state(["disabled"])
        self.info_label.config(text="Navigate the path carefully!")

    def end_game(self):
        if self.game_started and not self.game_over:
            self.game_over = True
            messagebox.showinfo("Congratulations!", "You Won!")
            self.reset_game()

    def check_position(self, event):
        if not self.game_started or self.game_over:
            return

        x, y = event.x, event.y

        if not self.is_on_path(x, y):
            self.game_over = True
            messagebox.showinfo("Game Over", "You Lost!")
            self.reset_game()

    def is_on_path(self, x, y):
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            if self.create_point(x, y, x1, y1, x2, y2):
                return True
        return False

    def create_point(self, px, py, x1, y1, x2, y2):
        buffer = 20
        if x1 == x2:
            return (x1 - buffer <= px <= x1 + buffer) and (min(y1, y2) <= py <= max(y1, y2))
        if y1 == y2:
            return (y1 - buffer <= py <= y1 + buffer) and (min(x1, x2) <= px <= max(x1, x2))
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        expected_y = slope * px + intercept
        return (abs(py - expected_y) <= buffer) and (min(x1, x2) <= px <= max(x1, x2))

    def reset_game(self):
        self.game_started = False
        self.game_over = False
        self.start_button.state(["!disabled"])
        self.path = self.create_path()
        self.start_x, self.start_y = self.path[0]
        self.end_x, self.end_y = self.path[-1]
        self.canvas.delete("all")
        self.draw_path()
        self.start_button.place(x=self.start_x - 30, y=self.start_y - 15)
        self.end_button.place(x=self.end_x - 30, y=self.end_y - 15)
        self.info_label.config(text="Click Start")

if __name__ == "__main__":
    root = tk.Tk()
    game = PrecisionPathGame(root)
    root.mainloop()