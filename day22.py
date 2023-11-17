"""
Day 22 - Ping-Pong

tags:
"""
from turtle import Screen, Turtle

# Setting up the screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Ping-Pong")
screen.tracer(0)

paddle = Turtle()
paddle.shape("square")
paddle.shapesize(stretch_wid=5, stretch_len=1)
paddle.penup()
paddle.goto(350, 0)


def go_up():
    """Move the paddle up."""
    new_y = paddle.ycor() + 20
    paddle.goto(paddle.xcor(), new_y)


def go_down():
    """Move the paddle down."""
    new_y = paddle.ycor() + 20
    paddle.goto(paddle.xcor(), new_y)


screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")

game_on = True
while game_on:
    screen.update()

screen.exitonclick()
