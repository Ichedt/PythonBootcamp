"""
Day 31 - Flash Cards Program

tags: capstone project
"""
import tkinter
import random
import pandas

BACKGROUND_COLOUR = "#b1ddc6"
TITLE_FONT = ("Arial", 40, "italic")
BODY_FONT = ("Arial", 60, "bold")
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("day31/data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("day31/data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    """Choose a random word from the data and change the card."""

    global current_card
    global flip_timer
    # Cancel the timer to prevent incorrect flips
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_body, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    """Flip the card for the current word translation."""

    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_body, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known_word():
    """Mark the current word as known so it wont appear again."""

    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("day31/data/words_to_learn.csv", index=False)

    next_card()


# Setup
window = tkinter.Tk()
window.title("Flash Cards")
window.config(padx=40, pady=40, bg=BACKGROUND_COLOUR)

flip_timer = window.after(5000, func=flip_card)

canvas = tkinter.Canvas(width=800, height=526)
card_front_img = tkinter.PhotoImage(file="day31/images/card_front.png")
card_back_img = tkinter.PhotoImage(file="day31/images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=TITLE_FONT)
card_body = canvas.create_text(400, 263, text="", font=BODY_FONT)
canvas.config(bg=BACKGROUND_COLOUR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

cross_image = tkinter.PhotoImage(file="day31/images/wrong.png")
unknown_button = tkinter.Button(
    image=cross_image, highlightthickness=0, command=next_card
)
unknown_button.grid(column=0, row=1)

check_image = tkinter.PhotoImage(file="day31/images/right.png")
known_button = tkinter.Button(
    image=check_image, highlightthickness=0, command=is_known_word
)
known_button.grid(column=1, row=1)

next_card()

window.mainloop()
