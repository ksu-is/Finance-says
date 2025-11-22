import tkinter as tk
from tkinter import messagebox
import random

# Define colors and their hex codes
COLORS = {
    "purple": "#aa2cee",
    "light_blue": "#00ffff",
    "orange": "#ff6f00",
    "green": "#00ff6e"
}


class SimonSaysGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Finance Says")

        # Game state
        self.sequence = []
        self.sequence_index = 0
        self.player_sequence_index = 0
        self.score = 0
        self.showing_sequence = False  # True while the computer is flashing colors

        # Score label
        self.score_label = tk.Label(
            self.master, text="Score: 0", font=("Arial", 20))
        self.score_label.pack(pady=10)

        # Canvas for colored pads
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack(pady=10)

        # Create 4 colored pads (2x2 grid)
        self.color_rects = {}  # map color -> rectangle id

        # Positions: (x1, y1, x2, y2)
        positions = {
            "purple": (0, 0, 200, 200),
            "light_blue": (200, 0, 400, 200),
            "orange": (0, 200, 200, 400),
            "green": (200, 200, 400, 400)
        }

        for color, coords in positions.items():
            rect_id = self.canvas.create_rectangle(
                *coords,
                fill=COLORS[color],
                outline="black",
                width=3
            )
            self.color_rects[color] = rect_id
            # Bind mouse clicks to each pad
            self.canvas.tag_bind(rect_id, "<Button-1>",
                                 lambda event, c=color: self.color_clicked(c))

        # Start button
        self.start_button = tk.Button(
            self.master,
            text="Start",
            font=("Arial", 16),
            command=self.start_game
        )
        self.start_button.pack(pady=20)

    def start_game(self):
        """Reset and start a new game."""
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.sequence = []
        self.add_color_and_play()

    def add_color_and_play(self):
        """Add a new random color to the sequence and play it."""
        new_color = random.choice(list(COLORS.keys()))
        self.sequence.append(new_color)
        self.sequence_index = 0
        self.player_sequence_index = 0
        self.showing_sequence = True
        # Disable start button while playing
        self.start_button.config(state=tk.DISABLED)
        self.master.after(500, self.highlight_next_color)

    def highlight_next_color(self):
        """Flash the next color in the sequence on the canvas."""
        if self.sequence_index >= len(self.sequence):
            # Finished showing; now wait for player's input
            self.showing_sequence = False
            self.start_button.config(state=tk.NORMAL)
            return

        color = self.sequence[self.sequence_index]
        rect_id = self.color_rects[color]

        # Flash: change fill to white, then back to color
        self.canvas.itemconfig(rect_id, fill="white")
        self.master.after(
            400,
            lambda r=rect_id, c=color: self.canvas.itemconfig(r, fill=COLORS[c])
        )

        self.sequence_index += 1
        self.master.after(700, self.highlight_next_color)

    def color_clicked(self, color):
        """Handle the player clicking a color pad."""
        # Ignore clicks while the sequence is being shown
        if self.showing_sequence:
            return

        expected_color = self.sequence[self.player_sequence_index]

        if color == expected_color:
            self.player_sequence_index += 1

            # If they matched the whole sequence correctly
            if self.player_sequence_index == len(self.sequence):
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.add_color_and_play()
        else:
            self.end_game()

    def end_game(self):
        messagebox.showinfo("Game Over", f"Your final score is {self.score}")
        self.showing_sequence = False
        self.start_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    game = SimonSaysGame(root)
    root.mainloop()
