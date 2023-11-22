"""
Day 24 - Mail Merge Project

tags: file management, file paths
"""
PLACEHOLDER = "[name]"

# Using relative path
with open("./Input/Names/invited_names.txt", encoding="utf-8") as names_file:
    names = names_file.readlines()

with open("./Input/Letters/starting_letter.txt", encoding="utf-8") as letter_file:
    letter_content = letter_file.read()
    for name in names:
        formatted_name = name.strip()
        new_letter = letter_content.replace(PLACEHOLDER, formatted_name)

        # Creating the text files
        with open(
            f"./Output/ReadyToSend/letter_for_{formatted_name}.txt",
            mode="w",
            encoding="utf-8",
        ) as final_letter:
            final_letter.write(new_letter)
