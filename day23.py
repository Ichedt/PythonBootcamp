"""
Day 23 - Turtle Crossing Game

tags: classes, inheritance, 
"""
from turtle import Screen, Turtle
import time
import random

# Car constants
COLORS = ["red", "black", "gray", "green", "orange", "blue"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
# Player constants
STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280
# Scoreboard constants
FONT = ("Monospace", 24, "normal")


class CarManager:
    """Create the car object."""

    def __init__(self):
        self.all_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_cars(self):
        """Set up the car object on the screen."""
        # To avoid too many cars, generate 1/8 times at random chance
        random_chance = random.randint(1, 8)
        if random_chance == 1:
            new_car = Turtle("square")
            new_car.shapesize(stretch_len=2, stretch_wid=1)
            new_car.penup()
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-250, 250)
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)

    def move_cars(self):
        """Move the created cars."""

        for cars in self.all_cars:
            cars.backward(self.car_speed)

    def level_up(self):
        """Increments the cars speed."""

        self.car_speed += MOVE_INCREMENT


class Player(Turtle):
    """Create player object."""

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.goto(STARTING_POSITION)
        self.setheading(90)

    def move_up(self):
        """Move the player up."""

        self.forward(MOVE_DISTANCE)

    def go_to_start(self):
        """Reposition the player to the starting location."""

        self.goto(STARTING_POSITION)

    def is_at_finish(self):
        """Detect if the player is at the finish line and return True or False."""

        if self.ycor() > FINISH_LINE_Y:
            return True
        else:
            return False


class Scoreboard(Turtle):
    """Create scoreboard object."""

    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.goto(-280, 250)
        self.update()

    def update(self):
        """Clear and update the level."""

        self.clear()
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def increase_level(self):
        """Increase the current level."""

        self.level += 1
        self.update()

    def game_over(self):
        """Show game over message."""

        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=FONT)


# Set up the screen
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

# Create objects
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

# Set up controls
screen.listen()
screen.onkeypress(player.move_up, "Up")

# Game loop
game_on = True
while game_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_cars()
    car_manager.move_cars()

    # Detect collision with cars
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_on = False

    # Detect success
    if player.is_at_finish():
        player.go_to_start()
        car_manager.level_up()
        scoreboard.increase_level()


screen.exitonclick()
