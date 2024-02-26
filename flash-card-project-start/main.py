from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

# Read data from CSV
data = pd.read_csv("data/french_words.csv")
to_learn = data.to_dict(orient="records")
current_card = {}

# Button functionality
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    update_card("French", current_card["French"])

def card_flip():
    update_card("English", current_card.get("English", "Translation not available"))
    canvas.itemconfig(card_background, image=card_back_image)

def is_known():
    to_learn.remove(current_card)
    pd.DataFrame(to_learn).to_csv("data/world_to_learn.csv", index=False)
    next_card()

def update_card(title, text):
    canvas.itemconfig(card_title, text=title, fill="black")
    canvas.itemconfig(card_word, text=text, fill="black")
    window.after(3000, func=card_flip)

# Creating window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Front image
canvas = Canvas(width=800, height=526)
card_back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_back_image)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

flip_timer = window.after(3000, func=card_flip)
card_flip()

# Creating buttons
unknown_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(row=1, column=1)

next_card()

window.mainloop()
