"""
Day 30 - Password Manager (Improved)

tags: errors, exceptions, json data
"""
import tkinter
from tkinter import messagebox
import random
import json


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
    """Save the entered data into a JSON file."""

    website = website_entry.get()
    username = username_entry.get()
    passcode = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": passcode,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(passcode) == 0:
        messagebox.showinfo(
            title="No Entry", message="There are blank fields. Return and fill them."
        )
    else:
        # Try open the file and reading data
        try:
            with open("day30/data.json", "r", encoding="utf-8") as data_file:
                # Read old data file
                data = json.load(data_file)
        # If there's no such file, create one
        except FileNotFoundError:
            with open("day30/data.json", "w", encoding="utf-8") as data_file:
                json.dump(new_data, data_file, indent=4)
        # If the file exists, update the data and write it on the file
        else:
            # Update old data file with new data
            data.update(new_data)

            with open("day30/data.json", "w", encoding="utf-8") as data_file:
                # Save updated data
                json.dump(new_data, data_file, indent=4)
        # Finally delete all entered information
        finally:
            website_entry.delete(0, tkinter.END)
            username_entry.delete(0, tkinter.END)
            password_entry.delete(0, tkinter.END)


# Find Password
def search():
    """Search the website and show the password if it exists."""

    website = website_entry.get()

    try:
        with open("day30/data.json", "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(
            title="File Not Found", message="There is no data file to search for."
        )
    else:
        # Verify if the website is saved and get the email and password
        if website in data:
            username = data[website]["username"]
            passcode = data[website]["password"]
            messagebox.showinfo(
                title=website, message=f"Username: {username}\nPassword: {passcode}"
            )
        else:
            messagebox.showinfo(
                title=f"{website} Not Found",
                message=f"There is no user nor password related to {website}",
            )


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
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

search_button = tkinter.Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky="EW", padx=(8, 0))

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
