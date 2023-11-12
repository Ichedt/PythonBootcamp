"""
Day 18 - The Hirst Paiting

tags: tuples, GUI, modules, turtle module
"""
import turtle as turtle_module
import random

t = turtle_module.Turtle()
turtle_module.colormode(255)
# Sets the animation speed
t.speed("fastest")
# Removes the drawing line
t.penup()
# Hides the turtle
t.hideturtle()

colors_list = [(184, 12, 9), (0, 114, 187), (250, 169, 22), (27, 27, 30)]
background = (230, 230, 230)

# Positions the turtle to the bottom left of the screen
t.setheading(225)
t.forward(300)
t.setheading(0)

number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    # Draws the dots with a random color from the list
    t.dot(20, random.choice(colors_list))
    t.forward(50)

    if dot_count % 10 == 0:
        t.setheading(90)
        t.forward(50)
        t.setheading(180)
        t.forward(500)
        t.setheading(0)

# Shows the screen
screen = turtle_module.Screen()
# Sets background color
screen.bgcolor(background)
# Persists the screen until its clicked
screen.exitonclick()
