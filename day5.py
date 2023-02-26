# Day 5 - Password Generator
#
# tags: for loops, range, code block

import random

def letter_picker():
    letter_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    choice = random.choice(letter_list)
    return choice


def upper_lower(letter):
    options = ["upper", "lower"]
    option = random.choice(options)

    if option == "upper":
        return letter.upper()
    
    else:
        return letter.lower()


def symbol_picker():
    symbol_list = ["!", "@", "#", "$", "%", "&", "*", "?", "+", "-", "^", "~", "=", "_"]

    choice = random.choice(symbol_list)
    return choice


def number_picker():
    number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    choice = random.choice(number_list)
    return choice


if __name__ == "__main__":
    print("Welcome to the Password Generator!")
    print("How many letters would you like in your password?")
    quantity_letters = int(input())

    print("How many symbols would you like?")
    quantity_symbols = int(input())

    print("How many numbers would you like?")
    quantity_numbers = int(input())

    total_characters = quantity_letters + quantity_symbols + quantity_numbers
    
    password = []

    for char in range(total_characters):
        choices = ["letter", "number", "symbol"]
        character_picker = random.choice(choices)

        if character_picker == "letter":
            letter = letter_picker()

            upper_lower(letter)

            password.append(letter)
        
        if character_picker == "number":
            number = number_picker()

            password.append(number)
        
        if character_picker == "symbol":
            symbol = symbol_picker()

            password.append(symbol)

    print(f"Your password is: {"".join(password)}")

    # NOTES
    # Theres an easier version for mixing the characters inside a list, the function is shuffle(). However in the code is the "hard" way.
