"""
Day 29 - Password Manager

tags: tkinter
"""
import tkinter
from tkinter import messagebox
import random


# Password Generator
def password_generator():
    """Generate a random password."""

    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)


# Save Password
def save():
    """Save the entered data into the data file."""

    website = website_entry.get()
    username = username_entry.get()
    passcode = password_entry.get()

    if len(website) == 0 or len(username) == 0 or len(passcode) == 0:
        messagebox.showinfo(
            title="No Entry", message="There are blank fields. Return and fill them."
        )
    else:
        is_ok = messagebox.askokcancel(
            title="Save Confirmation",
            message="These are the \
            details to be saved:\n \
            Username: {username}\n \
            Password: {passcode}\n \
            Website: {website}\n \
            Are they correct?",
        )
        if is_ok:
            with open("day29/data.txt", "a", encoding="utf-8") as data_file:
                data_file.write(f"{website} | {username} | {passcode}\n")
                website_entry.delete(0, tkinter.END)
                username_entry.delete(0, tkinter.END)
                password_entry.delete(0, tkinter.END)


# Setup
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = tkinter.Canvas(width=200, height=200)
logo_img = tkinter.PhotoImage(file="day29/logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = tkinter.Label(text="Website:")
website_label.grid(column=0, row=1, sticky="W", pady=4, padx=(0, 8))

website_entry = tkinter.Entry()
website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
website_entry.focus()

username_label = tkinter.Label(text="Email/Username:")
username_label.grid(column=0, row=2, sticky="W", pady=4, padx=(0, 8))

username_entry = tkinter.Entry()
username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

password_label = tkinter.Label(text="Password:")
password_label.grid(column=0, row=3, sticky="W", pady=4, padx=(0, 8))

password_entry = tkinter.Entry()
password_entry.grid(column=1, row=3, sticky="EW")

generate_button = tkinter.Button(text="Generate Password", command=password_generator)
generate_button.grid(column=2, row=3, sticky="EW", padx=(8, 0))

save_button = tkinter.Button(text="Save", width=35, command=save)
save_button.grid(column=1, row=4, columnspan=2, sticky="EW", pady=8)

window.mainloop()
