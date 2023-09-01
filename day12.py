# Day 12 - Number Guessing Game
#
# tags: scope, namespace
from random import randint

EASY_LEVEL_GUESSES = 10
HARD_LEVEL_GUESSES = 5


def check_answer(guess, answer, turns):
    """Checks the answer with the user's guess. Returns the number of turns remaining."""
    if guess > answer:
        print("Too high!")
        return turns - 1
    elif guess < answer:
        print("Too low!")
        return turns - 1
    else:
        print(f"You got it! The answer was {answer}.")


def choose_difficulty():
    """Let the user choose the dificulty of the game."""
    level = input("Choose the difficulty. Type 'easy' or 'hard': ")
    if level == "easy":
        return EASY_LEVEL_GUESSES
    elif level == "hard":
        return HARD_LEVEL_GUESSES
    else:
        print(f"{level} is not a valid option!")


def game():
    # Welcome message
    print("Welcome to the Number Guessing Game!")
    print("The number is between 1 and 100.")
    answer = randint(1, 100)

    turns = choose_difficulty()

    guess = 0
    while guess != answer:
        print(f"You have {turns} attempts to guess the number.")

        # Let the user guess a number.
        guess = int(input("Make a guess: "))

        # Track the number of turns and reduce by 1 if it's wrong.
        turns = check_answer(guess, answer, turns)

        if turns == 0:
            print("You've run out of guesses, you lose.")
            return
        elif guess != answer:
            print("Guess again.")


game()
