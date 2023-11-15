"""
Day 19 - Turtle Race

tags: turtle, event listener, state, instance
"""
from turtle import Turtle, Screen
import random

# Setting up screen and asking user choice
screen = Screen()
screen.setup(width=500, height=400)
user_choice = screen.textinput(
    title="Choose your winner!",
    prompt="Which turtle will win the race? Enter a color (violet, indigo,"
    "blue, green, yellow, orange, red):",
)

colors = ["purple", "indigo", "blue", "green", "yellow", "orange", "red"]
y_positions = [120, 80, 40, 0, -40, -80, -120]
all_turtles = []
is_race_on = False

# Positioning the turtles to the left of the window
for turtle_index in range(0, 7):
    turtle = Turtle(shape="turtle")
    turtle.color(colors[turtle_index])
    turtle.penup()
    turtle.goto(x=-200, y=y_positions[turtle_index])
    all_turtles.append(turtle)

if user_choice:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winner_color = turtle.pencolor()
            if winner_color == user_choice:
                print(f"You've won! The {winner_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winner_color} turtle is the winner!")

        random_distance = random.randint(0, 10)
        turtle.forward(random_distance)

screen.exitonclick()
