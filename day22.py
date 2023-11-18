"""
Day 22 - Ping-Pong

tags: turtle graphics, inheriterance, class
"""
from turtle import Screen, Turtle
import time

# Scoreboard constants
ALIGNMENT = "center"
FONT = ("Monospace", 80, "normal")


class Paddle(Turtle):
    """Creates a paddle object."""

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=1, stretch_wid=5)
        self.penup()
        self.goto(position)

    def go_up(self):
        """Move the paddle upwards."""

        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)

    def go_down(self):
        """Move the paddle downwards."""

        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)


class Ball(Turtle):
    """Creates a ball object."""

    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def move(self):
        """Move the ball to the top right corner."""

        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Bounce the ball in the Y coordinate."""

        self.y_move *= -1

    def bounce_x(self):
        """Bounce the ball in the X coordinate and increse ball speed."""

        self.x_move *= -1
        self.move_speed *= 0.9

    def reset_position(self):
        """Reset the ball configuration

        Reset the ball position to the center and bounce to the opposite side.
        Also reduce the speed to its initial value.
        """

        self.goto(0, 0)
        self.move_speed = 0.1
        self.bounce_x()


class Scoreboard(Turtle):
    """Create a scoreboard."""

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.left_score = 0
        self.right_score = 0
        self.update_score()

    def update_score(self):
        """Uptade the score with new points."""

        self.clear()
        self.goto(-100, 200)
        self.write(self.left_score, align=ALIGNMENT, font=FONT)
        self.goto(100, 200)
        self.write(self.right_score, align=ALIGNMENT, font=FONT)

    def left_point(self):
        """Add one point to the left score."""

        self.left_score += 1
        self.update_score()

    def right_point(self):
        """Add one point to the right score."""

        self.right_score += 1
        self.update_score()


# Setting up the screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Ping-Pong")
screen.tracer(0)

# Initialising the objects
left_paddle = Paddle((-350, 0))
right_paddle = Paddle((350, 0))
ball = Ball()
scoreboard = Scoreboard()

# Setting paddle controls
screen.listen()
screen.onkeypress(right_paddle.go_up, "Up")
screen.onkeypress(right_paddle.go_down, "Down")
screen.onkeypress(left_paddle.go_up, "w")
screen.onkeypress(left_paddle.go_down, "s")

game_on = True
while game_on:
    time.sleep(ball.move_speed)
    screen.update()

    ball.move()

    # Detect collision with the top and bottom walls
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect collision with the paddles
    # Detects if the ball is past 340p on the screen and if the paddle is hit
    if (
        ball.distance(right_paddle) < 50
        and ball.xcor() > 320
        or ball.distance(left_paddle) < 50
        and ball.xcor() < -320
    ):
        ball.bounce_x()

    # Detect collision with the left and right walls
    ## Detect when the RIGHT paddle misses the ball
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.right_point()

    ## Detect when the LEFT paddle misses the ball
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.left_point()

screen.exitonclick()
