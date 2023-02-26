# Day 4 - Rock Paper Scissors
#
# tags: randomisation, modules,  lists

import random


print("What do you choose? [R]ock, [P]aper or [S]cissors?")
user_choice = input().lower()

options = ["Rock", "Paper", "Scissors"]
computer_choice = random.choice(options)

if user_choice == computer_choice:
    print("Draw!")

elif user_choice == "r":
    if computer_choice == "Paper":
        print("Computer chose Paper, you lost!")
    else:
        print("Computer chose Scissors, you win!")

elif user_choice == "p":
    if computer_choice == "Rock":
        print("Computer chose Rock, you win!")
    else:
        print("Computer chose Scissors, you lost!")

elif user_choice == "s":
    if computer_choice == "Rock":
        print("Computer chose Rock, you lost!")
    else:
        print("Computer chose Paper, you win!")

else:
    print("Invalid option!")
