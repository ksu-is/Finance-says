import tkinter as tk
from tkinter import messagebox
import random

# Define colors and their hex codes
COLORS = {
    "purple": "#aa2cee",
    "light_blue": "#00ffff",
    "orange": "#ff6f00",
    "green": "#00ff6e",
    "pink": "#ff006a"
}


class SimonSaysGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Finance Says") #Game title 

        # Game state
        self.sequence = [] #where the computer generates and stores random colors (sequence)
        self.sequence_index = 0 #tracks the step of the sequence the computer is currently flashing
        self.player_sequence_index = 0 #keeps track of the players inputs
        self.score = 0 #Tracks what round the players on 
        self.showing_sequence = False  # True while the computer is flashing colors

        # Score label
        self.score_label = tk.Label(
            self.master, text="Score: 0", font=("Arial", 20)) #main window of tk
        self.score_label.pack(pady=10) #decided positioning to be moved from top to bottom, which creates 10 px of spcae above/below

        # Creates a Canvas for the colored pads (kind of like a blank sheet)
        self.canvas = tk.Canvas(self.master, width=400, height=400) #canvas size is 400 x 400
        self.canvas.pack(pady=10) #put into window with 10 pixels of padding (the space between score and the start button)

        # Create 4 colored pads (2x2 grid)
        self.color_rects = {}  # map color -> rectangle id (holds/stores rectangle ids)

        # Positions: (x1, y1, x2, y2) essentially a 4x4 box
        positions = {
            "purple": (0, 0, 200, 200),
            "light_blue": (200, 0, 400, 200),
            "orange": (0, 200, 200, 400),
            "green": (200, 200, 400, 400),
            "pink": (100, 100, 300, 300) 
        }

        for color, coords in positions.items():
            rect_id = self.canvas.create_rectangle(
                *coords, #creates outline of square 
                fill=COLORS[color], 
                outline="black", #black boarder 
                width=3 #of boarder
            )
            self.color_rects[color] = rect_id #maps the rectangle id to the color
            # Bind mouse clicks to each pad
            self.canvas.tag_bind(rect_id, "<Button-1>", #which shape to listen to-left mouse click-what function to run when clicked
                                 lambda event, c=color: self.color_clicked(c))

        # Start button
        self.start_button = tk.Button(
            self.master,
            text="Start",
            font=("Arial", 16),
            command=self.start_game #call function when button is clicked
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
        if self.sequence_index >= len(self.sequence): #checks if computer flashed every color
            # Finished showing; now wait for player's input
            self.showing_sequence = False
            self.start_button.config(state=tk.NORMAL)
            return

        color = self.sequence[self.sequence_index]
        rect_id = self.color_rects[color] #finds what color to flash

        # Flash: change fill to white, then back to color
        self.canvas.itemconfig(rect_id, fill="white") #flash animation
        self.master.after(
            400,#400 milliaseconds
            lambda r=rect_id, c=color: self.canvas.itemconfig(r, fill=COLORS[c])#runs after, reverses the flash
        )

        self.sequence_index += 1  #moves on to the next color
        self.master.after(700, self.highlight_next_color)

    def color_clicked(self, color):
        """Handle the player clicking a color pad."""
        # Ignore clicks while the sequence is being shown
        if self.showing_sequence:
            return
        
        rect_id = self.color_rects[color]
        original_color = COLORS[color]

        # --- Flash on click ---
        self.canvas.itemconfig(rect_id, fill="black")
        self.master.after(
            200, 
            lambda r=rect_id, c=original_color: self.canvas.itemconfig(r, fill=c)
        )
        # ----------------------

    

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
    root = tk.Tk() #creates main application window
    game = SimonSaysGame(root) #runs game in window
    root.mainloop() #runs forever
