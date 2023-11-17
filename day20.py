"""
Day 20 - Snake Game

tags: oop, turtle graphics, slicing
"""
from turtle import Screen, Turtle
import time
import random

# Snake constants
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

# Scoreboard constants
ALIGNMENT = "center"
FONT = ("Arial", 24, "normal")


class Snake:
    """Create a snake instance."""

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        """Create the snake."""
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        """Add a segment to the snake."""
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def extend(self):
        """Add a new segment to the snake."""
        self.add_segment(self.segments[-1].position())

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


class Food(Turtle):
    """Create a food on the screen."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.75, stretch_wid=0.75)
        self.color("yellow")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        """Position the food at random location."""
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)


class Scoreboard(Turtle):
    """Create a scoreboard on the screen."""

    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.goto(0, 270)
        self.color("white")
        self.update_score()
        self.hideturtle()

    def update_score(self):
        """Write the scoreboard on the screen."""
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        """Increase the score by 1."""
        self.score += 1
        self.clear()
        self.update_score()

    def game_over(self):
        """Write game over on the screen."""
        self.goto(0, 0)
        self.write("Game Over", align=ALIGNMENT, font=FONT)


# Set up the screen
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# Create the snake, food and scoreboard objects
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# Detect key presses
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

# Game loop
game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    # Detect collision with food
    # The number is the minimal distance for the detection
    if snake.head.distance(food) < 20:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    # Detect collision with wall
    if (
        snake.head.xcor() > 280
        or snake.head.xcor() < -280
        or snake.head.ycor() > 280
        or snake.head.ycor() < -280
    ):
        game_on = False
        scoreboard.game_over()

    # Detect collision with tail
    ## Slicing the list so the head is not included
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_on = False
            scoreboard.game_over()

screen.exitonclick()
