"""
Day 19 - Turtle Race

tags: turtle, event listener, state, instance
"""
from turtle import Turtle, Screen

t = Turtle()
screen = Screen()


def move_forwards():
    """Moves the turtle forwards."""
    t.forward(10)


def move_backwards():
    """Moves the turtle backwards."""
    t.backward(10)


def turn_left():
    """Turns the turtle to the left."""
    new_heading = t.heading() + 10
    t.setheading = new_heading


def turn_right():
    """Turns the turtle to the right."""
    new_heading = t.heading() - 10
    t.setheading = new_heading


def clear_screen():
    """Clears the screen."""
    t.clear()
    t.penup()
    t.home()
    t.pendown()


screen.listen()
screen.onkey(move_forwards, "w")
screen.onkey(move_backwards, "s")
screen.onkey(turn_left, "a")
screen.onkey(turn_right, "d")
screen.onkey(clear_screen, "c")
screen.exitonclick()
