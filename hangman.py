
import tkinter as tk
import random
import math

# =========================================
# HANGMAN - CARTOON LANDSCAPE EDITION
# =========================================

WORDS = ["PYTHON", "COMPUTER", "PROGRAM", "KEYBOARD", "DEVELOPER"]

W, H = 1000, 620
MAX_ATTEMPTS = 6

SKY = "#55A9F0"
DARK_BLUE = "#0756A5"
BLUE = "#0879D9"
LIGHT_BLUE = "#42A9F4"
GREEN = "#55B83F"
DARK_GREEN = "#258B35"
ORANGE = "#FFAD24"
BROWN = "#98501F"
CREAM = "#FFF0CF"
WHITE = "#FFFFFF"
RED = "#E73548"


class HangmanGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry(f"{W}x{H+35}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=W,
            height=H,
            bg=SKY,
            highlightthickness=0
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_hover)

        self.new_game()
        self.draw_game()

    # =====================================
    # GAME DATA
    # =====================================

    def new_game(self):
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.wrong = 0
        self.finished = False
        self.message = "Choose a Letter"
        self.message_color = "#56351F"

    def restart(self):
        self.new_game()
        self.draw_game()

    # =====================================
    # DRAWING HELPERS
    # =====================================

    def rect(self, x1, y1, x2, y2, color,
             outline="", width=1):
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline=outline,
            width=width
        )

    def oval(self, x1, y1, x2, y2, color,
             outline="", width=1):
        self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=color,
            outline=outline,
            width=width
        )

    def line(self, points, color, width=3):
        self.canvas.create_line(
            *points,
            fill=color,
            width=width,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND
        )

    def text(self, x, y, value, size, color,
             bold=True, font="Arial"):
        self.canvas.create_text(
            x, y,
            text=value,
            fill=color,
            font=(font, size, "bold" if bold else "normal")
        )

    # =====================================
    # BACKGROUND
    # =====================================

    def draw_background(self):

        c = self.canvas

        self.rect(0, 0, W, H, SKY)

        # Sun
        self.oval(865, 25, 925, 85, "#FFD84B", "#F4A900", 3)

        # Clouds
        self.draw_cloud(40, 65, 0.8)
        self.draw_cloud(185, 40, 1.0)
        self.draw_cloud(775, 65, 0.9)

        # Distant hills
        c.create_oval(
            -100, 440, 390, 690,
            fill="#82D46B", outline=""
        )
        c.create_oval(
            270, 435, 780, 700,
            fill="#72C85A", outline=""
        )
        c.create_oval(
            650, 440, 1120, 700,
            fill="#83D66A", outline=""
        )

        # Main grass
        self.rect(0, 525, W, H, GREEN)

        # Grass details
        for x in range(5, W, 30):
            y = 535 + (x % 4) * 4
            self.line([x, y, x-7, y-13], "#318D35", 2)
            self.line([x+4, y, x+10, y-10], "#318D35", 2)

        # Stones
        self.oval(15, 535, 48, 555, "#8B8067", "#615644", 2)
        self.oval(55, 540, 75, 553, "#A59A7B", "#615644", 2)
        self.oval(910, 520, 955, 548, "#8D8065", "#615644", 2)

        # Bushes
        self.draw_bush(40, 560)
        self.draw_bush(870, 565)
        self.draw_bush(950, 570)

    def draw_cloud(self, x, y, scale):

        c = self.canvas

        parts = [
            (0, 18, 45, 48),
            (20, 0, 75, 48),
            (48, 12, 95, 48)
        ]

        for x1, y1, x2, y2 in parts:
            c.create_oval(
                x + x1*scale,
                y + y1*scale,
                x + x2*scale,
                y + y2*scale,
                fill="#D8F0FF",
                outline=""
            )

    def draw_bush(self, x, y):

        for dx, dy, size in [
            (0, 10, 25),
            (18, 0, 30),
            (38, 12, 24),
            (22, 20, 28)
        ]:
            self.oval(
                x+dx, y+dy,
                x+dx+size, y+dy+size,
                DARK_GREEN
            )

    # =====================================
    # TITLE
    # =====================================

    def draw_title(self):

        # Shadow
        self.text(
            503, 58, "HANGMAN",
            65, "#9B4D17"
        )

        # Main title
        self.text(
            500, 52, "HANGMAN",
            65, "#FF9D16"
        )

       
        # Subtitle wooden banner
        self.rect(
            350, 108, 650, 147,
            "#B46B2E", "#784019", 3
        )

        # Inner cream board
        self.rect(
            358, 112, 642, 143,
            "#FFE1A0", "#A96525", 2
        )

        # Subtitle inside wooden board
        self.text(
            500, 127,
            "Guess the Word • Save the Stickman",
            12, "#54331B"
        )


    # =====================================
    # WOODEN GALLOWS
    # =====================================

    def draw_gallows(self):

        # Base
        self.rect(35, 510, 260, 535, "#A75B25", "#6D3515", 3)

        # Main post
        self.rect(48, 190, 72, 515, "#B86B2C", "#703B19", 3)

        # Top beam
        self.rect(48, 155, 245, 178, "#C37A34", "#784019", 3)

        # Wooden support
        self.line([65, 185, 130, 250], "#8E4D20", 14)

        # Wood texture
        self.line([55, 165, 220, 165], "#E5A052", 2)
        self.line([58, 185, 58, 495], "#E5A052", 2)

        # Nails
        for x, y in [(60, 165), (230, 165), (60, 520), (250, 520)]:
            self.oval(
                x, y, x+7, y+7,
                "#633A21"
            )

        # Rope
        self.line([220, 177, 220, 210], "#77502C", 4)

        # Stickman
        self.draw_stickman()

    # =====================================
    # CARTOON STICKMAN
    # =====================================

    def draw_stickman(self):

        c = self.canvas
        color = "#45281D"
        width = 6

        if self.wrong >= 1:

            # Head
            self.oval(
                190, 205, 250, 265,
                "#FFF1D6", color, 4
            )

            # Cross eyes
            self.line([203, 222, 213, 232], color, 3)
            self.line([213, 222, 203, 232], color, 3)

            self.line([228, 222, 238, 232], color, 3)
            self.line([238, 222, 228, 232], color, 3)

            # Sad mouth
            c.create_arc(
                208, 238, 232, 255,
                start=0, extent=180,
                outline=color, width=3
            )

        if self.wrong >= 2:
            self.line([220, 265, 220, 355], color, width)

        if self.wrong >= 3:
            self.line([220, 285, 175, 325], color, width)

        if self.wrong >= 4:
            self.line([220, 285, 265, 325], color, width)

        if self.wrong >= 5:
            self.line([220, 355, 180, 420], color, width)

        if self.wrong >= 6:
            self.line([220, 355, 265, 420], color, width)

    # =====================================
    # STATISTIC CARDS
    # =====================================

    def draw_stats(self):

        cards = [
            (805, 155, 975, 230, "#258A37", "🏆", "Attempts", str(MAX_ATTEMPTS-self.wrong)),
            (805, 238, 975, 313, "#A83A30", "✖", "Wrong Guesses", str(self.wrong)),
            (805, 321, 975, 396, "#0864B5", "✔", "Letters Found",
             str(sum(1 for x in set(self.word) if x in self.guessed)))
        ]

        for x1, y1, x2, y2, color, symbol, label, value in cards:

            self.rect(
                x1, y1, x2, y2,
                color, "#FFFFFF", 2
            )

            self.oval(
                x1+10, y1+12,
                x1+48, y1+50,
                "#FFFFFF"
            )

            self.text(
                x1+29, y1+31,
                symbol, 19, color
            )

            self.text(
                x1+108, y1+20,
                label, 12, WHITE
            )

            self.text(
                x1+108, y1+49,
                value, 21, WHITE
            )

    # =====================================
    # PARCHMENT WORD PANEL
    # =====================================

    def draw_word_panel(self):

        # Outer wooden border
        self.rect(
            335, 230, 790, 365,
            "#B77A3D", "#8B4B20", 4
        )

        # Parchment
        self.rect(
            345, 238, 780, 357,
            CREAM, "#D6A35F", 3
        )

        self.text(
            560, 258,
            "Guess the Word",
            24, "#442816"
        )

        
        # Display letters evenly inside the wooden board

        word_length = len(self.word)

        # Available horizontal space inside the board
        left_position = 365
        right_position = 755

        # Calculate spacing automatically
        if word_length == 1:
            spacing = 0
        else:
            spacing = (right_position - left_position) / (word_length - 1)

        # Draw each letter separately
        for i, letter in enumerate(self.word):

            x = (
                560 if word_length == 1
                else left_position + i * spacing
            )

            display_letter = (
                letter if letter in self.guessed else "_"
            )

            self.text(
                x, 315,
                display_letter,
                30,
                "#392315"
            )


    # =====================================
    # KEYBOARD
    # =====================================


    def draw_keyboard(self):

        self.rect(
        480, 370, 655, 402,
        "#B77736", "#76421D", 3
        )

        self.text(
        568, 386,
        "Select a Letter",
        18, WHITE
        )

        self.key_boxes = {}

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        start_x = 350
        start_y = 410
        key_w = 48
        key_h = 34
        gap_x = 7
        gap_y = 5

        for i, letter in enumerate(letters):

            row = i // 7
            col = i % 7

            x = start_x + col * (key_w + gap_x)
            y = start_y + row * (key_h + gap_y)

            if letter in self.guessed:
                color = (
                    "#278B45"
                    if letter in self.word
                    else "#B63C36"
                )
            else:
                color = BLUE

            self.rect(
                x+2, y+3,
                x+key_w+2, y+key_h+3,
                DARK_BLUE
            )

            self.rect(
                x, y,
                x+key_w, y+key_h,
                color, WHITE, 2
            )

            self.text(
                x+key_w/2,
                y+key_h/2,
                letter,
                18, WHITE
            )

            self.key_boxes[letter] = (
                x, y, x+key_w, y+key_h
            )


    # =====================================
    # RESTART BUTTON
    # =====================================

    
    def draw_restart(self):

        self.rect(
            42, 566, 330, 615,
            "#663719", "#633314", 3
        )

        self.rect(
            38, 558, 326, 608,
            "#B76B2B", "#703A17", 4
        )

        self.rect(
            45, 565, 319, 600,
            "#CA843B", "#E7A45C", 2
        )

        self.text(
            182, 582,
            "⟳  RESTART GAME",
            20, "#3C2110"
        )

        self.restart_box = (38, 558, 326, 615)


    # =====================================
    # FULL GAME DRAW
    # =====================================

    def draw_game(self):

        self.canvas.delete("all")

        self.draw_background()
        self.draw_title()
        self.draw_gallows()
        self.draw_stats()
        self.draw_word_panel()
        self.draw_keyboard()
        self.draw_restart()

        
        if self.finished:

            if self.won:
                result = "YOU WON! CONGRATULATIONS!"
                color = "#176B30"
            else:
                result = "GAME OVER! WORD: " + self.word
                color = "#A32626"

            self.rect(
                350, 565, 790, 608,
                CREAM, "#A76A2D", 3
            )

            self.text(
                570, 586,
                result,
                17, color
            )

        else:

            self.text(
                570, 586,
                self.message,
                16, self.message_color
            )


    # =====================================
    # MOUSE CLICK
    # =====================================

    def handle_click(self, event):

        x, y = event.x, event.y

        # Restart
        if (
            self.restart_box[0] <= x <= self.restart_box[2]
            and self.restart_box[1] <= y <= self.restart_box[3]
        ):
            self.restart()
            return

        if self.finished:
            return

        # Keyboard
        for letter, box in self.key_boxes.items():

            x1, y1, x2, y2 = box

            if x1 <= x <= x2 and y1 <= y <= y2:

                self.guess(letter)
                return

    # =====================================
    # HOVER
    # =====================================

    def handle_hover(self, event):

        x, y = event.x, event.y

        hovering = False

        if hasattr(self, "key_boxes"):

            for letter, box in self.key_boxes.items():

                x1, y1, x2, y2 = box

                if x1 <= x <= x2 and y1 <= y <= y2:
                    if letter not in self.guessed and not self.finished:
                        hovering = True
                    break

        self.canvas.config(
            cursor="hand2" if hovering else "arrow"
        )

    # =====================================
    # GUESS
    # =====================================

    def guess(self, letter):

        if self.finished or letter in self.guessed:
            return

        self.guessed.add(letter)

        if letter in self.word:

            self.message = "Great! " + letter + " is correct!"
            self.message_color = "#176B30"

        else:

            self.wrong += 1

            self.message = "Wrong guess! Try again."
            self.message_color = "#A32626"

        # Win
        if all(letter in self.guessed for letter in self.word):

            self.finished = True
            self.won = True
            self.message = "Congratulations! You won!"

        # Loss
        elif self.wrong >= MAX_ATTEMPTS:

            self.finished = True
            self.won = False
            self.message = "Game Over! Word: " + self.word

        self.draw_game()


# =========================================
# START GAME
# =========================================

if __name__ == "__main__":

    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
