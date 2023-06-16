# Day 8 - Caesar Cipher
#
# tags: functions, inputs


def caesar(starting_text, shift_amount, cipher_direction, alphabet):
    end_text = ""

    if cipher_direction == "decode":
        shift_amount *= -1

    elif cipher_direction == "encode":
        pass

    else:
        return print("Invalid option!")

    for character in starting_text:
        if character in alphabet:
            position = alphabet.index(character)
            new_position = position + shift_amount
            end_text += alphabet[new_position]

        else:
            end_text += character

    print(f"The {direction}d text is {end_text}.")


if __name__ == "__main__":
    alphabet = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    option = True
    while option == True:
        direction = input(
            "Type 'encode' to encrypt, type 'decode' to decrpyt:\n"
        ).lower()
        text = input("Type your message:\n")
        shift = int(input("Type the shift number:\n"))

        shift = shift % 26

        caesar(
            starting_text=text,
            shift_amount=shift,
            cipher_direction=direction,
            alphabet=alphabet,
        )

        option = input(
            "Type 'yes' if you want to go again. Otherwise type 'no'.\n"
        ).lower()
        if option == "yes":
            pass

        elif option == "no":
            print("Goodbye!")
            option = False

        else:
            print("Invalid option. Exiting...")
