from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#b1d1fc"
COLOR1 = "#042e60"
COLOR2 = "#cb416b"
TITLE = "Korean"
PRONUNCIATION = "Pronunciation"
TRANSLATED_WORD = "English"
HINDI_WORD = "Hindi"
OTHER_LANGUAGE_CSV = "data/other_language.csv"
WORD_TO_LEARN = "data/words_to_learn.csv"
CARD_FRONT_IMG = "images/card_front.png"
CARD_BACK_IMG = "images/card_back.png"
RIGHT_IMG = "images/right.png"
WRONG_IMG = "images/wrong.png"


current_word_selection = {}
to_learn = {}

try:
    data = pandas.read_csv(WORD_TO_LEARN)
except (FileNotFoundError, pandas.errors.EmptyDataError):
    original_data = pandas.read_csv(OTHER_LANGUAGE_CSV)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def unknown_random_word():  # get a random card
    global current_word_selection, flip_timer
    window.after_cancel(flip_timer)

    current_word_selection = random.choice(to_learn)
    print(current_word_selection)

    canvas.itemconfig(card_title, text=TITLE, fill="black")
    canvas.itemconfig(card_word, text=current_word_selection[TITLE], fill="black")
    canvas.itemconfig(word_pronunciation, text=f"( {current_word_selection[PRONUNCIATION]} )", fill=COLOR2)
    canvas.itemconfig(hindi_meaning, text="")
    canvas.itemconfig(canvas_image, image=card_front_img)

    flip_timer = window.after(3000, func=word_flip)


def word_flip():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(card_title, text=TRANSLATED_WORD, fill=COLOR1,)
    canvas.itemconfig(card_word, text=current_word_selection[TRANSLATED_WORD], fill=COLOR1)
    canvas.itemconfig(word_pronunciation, text="")
    canvas.itemconfig(hindi_meaning, text=f"( {current_word_selection[HINDI_WORD]} )", fill=COLOR2)


def is_known():
    to_learn.remove(current_word_selection)  # remove word so that it don't appear again.
    new_data = pandas.DataFrame(to_learn)   # create new data file which contain words not appeared yet.
    new_data.to_csv(WORD_TO_LEARN, index=False)
    unknown_random_word()   # to show a new word


window = Tk()
window.title("my Flasky")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=word_flip)

canvas = Canvas(width=533, height=315, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file=CARD_FRONT_IMG)
card_back_img = PhotoImage(file=CARD_BACK_IMG)
canvas_image = canvas.create_image(267, 157, image=card_front_img, )
card_title = canvas.create_text(267, 50, text="", font=("ariel", 25, "italic"))
card_word = canvas.create_text(267, 150, text="", font=("ariel", 50, "bold"))
word_pronunciation = canvas.create_text(267, 230, text="", font=("ariel", 20, "italic"))
hindi_meaning = canvas.create_text(267, 230, text="", font=("ariel", 20, "italic"))
canvas.grid(column=0, row=0, columnspan=2, padx=5)

wrong_img = PhotoImage(file=WRONG_IMG)
wrong_button = Button(image=wrong_img, bd=0, bg=BACKGROUND_COLOR, highlightthickness=0, command=unknown_random_word)
wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file=RIGHT_IMG)
right_button = Button(image=right_img, bd=0, bg=BACKGROUND_COLOR, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

unknown_random_word()

window.mainloop()
