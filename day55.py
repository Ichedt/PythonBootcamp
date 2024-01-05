"""
Day 55 - Guess The Number Website

tags: flask, web development, decorators, routes
"""
import random
from types import FunctionType
from flask import Flask

app = Flask(__name__)
random_number = random.randint(0, 9)


# Creating a Decorator
def bold(function: FunctionType) -> str:
    """Decorator to make the text bold using HTML."""

    def wrapper() -> str:
        text = function()
        return f"<b>{text}</b>"

    return wrapper


# Home page
@app.route("/")
def home() -> str:
    """Render hello world string into the webpage."""
    return (
        "<h1>Guess a number between 0 and 9!</h1>"
        "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'>"
    )


# You can use different routes using the decorator
@app.route("/bye")
@bold
def bye() -> str:
    """Render bye string into the webpage."""
    return "Bye!"


# You can use variable paths and specify its data type
# Generating the pages based on the guess
@app.route("/<int:number>")
def guess(number: int) -> str:
    """Render the string with variables specified in the webpath."""
    if number > random_number:
        html_to_return = (
            "<h1 style='color:purple'>Too high, try again!</h1>"
            "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>"
        )
    elif number < random_number:
        html_to_return = (
            "<h1 style='color:red'>Too low, try again!</h1>"
            "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>"
        )
    else:
        html_to_return = (
            "<h1 style='color:green'>You found me!</h1>"
            "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>"
        )
    return html_to_return


if __name__ == "__main__":
    # Run the app in debug mode to auto-reload
    app.run(debug=True)
