import tkinter as tk
from tkinter import messagebox, simpledialog
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
        #changed background color
        self.master.configure(bg="#0F172A")

        # Game state
        self.sequence = [] #where the computer generates and stores random colors (sequence)
        self.sequence_index = 0 #tracks the step of the sequence the computer is currently flashing
        self.player_sequence_index = 0 #keeps track of the players inputs
        self.score = 0 #Tracks what round the players on 
        self.showing_sequence = False  # True while the computer is flashing colors
        self.questions = [
            {
                "question": "What does APR stand for?",
                "answer": "annual percentage rate"
            },
            {
                "question": "If you save $10 a week, how much will you have after 5 weeks?",
                "answer": "50"
            },
            {
                "question": "Is a stock generally more risky than a savings account? (yes/no)",
                "answer": "yes"
            }
        ]
        self.current_question_index = 0

        # Score label
        self.score_label = tk.Label(
            self.master, text="Score: 0", font=("Arial", 20,"bold"),bg="#0F172A",fg="#E178C8")
         #main window of tk
        self.score_label.pack(pady=10) #decided positioning to be moved from top to bottom, which creates 10 px of spcae above/below

        # Creates a Canvas for the colored pads (kind of like a blank sheet)
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="#020617", highlightthickness=0) #canvas size is 400 x 400
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
    self.master, text="Start",
    font=("Arial", 16, "bold"),
    bg="#38BDF8", fg="black",
    activebackground="#7DD3FC", activeforeground="black",
    bd=0, highlightthickness=0, relief="flat",
    command=self.start_game
)


        self.start_button.pack(pady=20)

    def start_game(self):
        """Show a prompt, then reset and start a new game."""
        ##adding starting prompt
        ready = messagebox.askyesno(
            "Ready to Play?",
            "You will be asked a finance-based question.\n"
            "Once answered correctly you will see a sequence of colors.\n"
            "Repeat the sequence by clicking the pads in order.\n"
            "Are you ready to start?"
        )

        if not ready:
            #if no is pressed do nothing
            return

        # If they clicked Yes, then start the game
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.sequence = []
        self.ask_finance_question()

    def ask_finance_question(self):
        """Ask the next finance question. Wrong answer ends the game."""
        # Loop back to first question if we reach the end
        if self.current_question_index >= len(self.questions):
            self.current_question_index = 0

        q = self.questions[self.current_question_index]
        self.current_question_index += 1

        answer = simpledialog.askstring(
            "Finance Question",
            q["question"],
            parent=self.master
        )

        # If user closes the dialog, end the game
        if answer is None:
            self.end_game()
            return

        # Check answer (case-insensitive)
        if answer.strip().lower() == q["answer"]:
            messagebox.showinfo(
                "Correct!",
                "Correct! Get ready for the color sequence."
            )
            self.add_color_and_play()
        else:
            messagebox.showinfo(
                "Incorrect",
                f"Incorrect.\nThe correct answer was:\n{q['answer']}"
            )
            self.end_game()

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
            self.ask_finance_question()

    def end_game(self):
        messagebox.showinfo("Game Over", f"Your final score is {self.score}")
        self.showing_sequence = False
        self.start_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk() #creates main application window
    game = SimonSaysGame(root) #runs game in window
    root.mainloop() #runs forever
