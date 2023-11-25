"""
Day 26 - NATO Alphabet Project

tags: list comprehension, dictionary comprehension
"""
import pandas

data = pandas.read_csv("day26/nato_phonetic_alphabet.csv")

# Creating the dictionary
nato_alphabet = {row.letter: row.code for (index, row) in data.iterrows()}

# Asking user's word
word = input("Enter a word: ").upper()

# Creating the list with letters and phonetic correspondents
output_list = [nato_alphabet[letter] for letter in word]
