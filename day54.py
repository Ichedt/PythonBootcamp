"""
Day 54 - Web Development with Flask

tags: backend, flask, web development, web server
"""
import time
from types import FunctionType
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    """Return "Hello, world!" string to the main webpage."""
    return "Hello, world!"


# Function Decorator part
def calculate_speed_decorator(function: FunctionType) -> FunctionType:
    """A function decorator to calculate the speed of a given function."""

    def wrapper_function() -> None:
        start_time = time.time()
        function()
        end_time = time.time()
        print(f"{function.__name__} run speed: {end_time - start_time}s")

    return wrapper_function


@calculate_speed_decorator
def fast_function() -> None:
    """A function to test the calculate_speed_decorator function."""
    for i in range(1000000):
        i * i


@calculate_speed_decorator
def slow_function() -> None:
    """A function to test the calculate_speed_decorator function."""
    for i in range(10000000):
        i * i


if __name__ == "__main__":
    app.run()
    fast_function()
    slow_function()
