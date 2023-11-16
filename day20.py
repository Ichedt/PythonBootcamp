"""
Day 20 - Snake Game

tags: oop, turtle graphics
"""
from turtle import Screen, Turtle
import time

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    """Create a snake instance."""

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        """Create the snake."""
        for position in STARTING_POSITIONS:
            new_segment = Turtle("square")
            new_segment.color("white")
            new_segment.penup()
            new_segment.goto(position)
            self.segments.append(new_segment)

    def move(self):
        """Move the snake forwards."""
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        """Head the snake up."""
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        """Head the snake down."""
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        """Head the snake to the left."""
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        """Head the snake to the right."""
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)


# Set up the screen
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

snake = Snake()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

# Set up snake starting position
game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)

    snake.move()


screen.exitonclick()
