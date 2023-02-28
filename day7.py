# Day 7 - Hangman
#
# tags: for loop, while loop, condition, list, module, range, string

import random


word_list = ["avocado", "baloon", "camel"]
chosen_word = random.choice(word_list)
word_length = len(chosen_word)
display = []
end_game = False
lives = 6

for _ in range(word_length):
    display += "_"

while not end_game:
    guess = input("Guess a letter: ").lower()

    if guess in display:
        print(f"You already guessed {guess}!")

    for position in range(word_length):
        if chosen_word[position] == guess:
            display[position] = guess

    if guess not in chosen_word:
        print(f"You guessed {guess}. That letter is not in the word.")
        lives -= 1
        if lives == 0:
            end_game = True
            print("You lose.")

    print(display)

    if "_" not in display:
        end_game = True
        print("You guessed the word!")
