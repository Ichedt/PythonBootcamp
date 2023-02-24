# Day 2 - Tip Calculator
#
# tags: data types, numbers, operations, type conversion, f-Strings

def tip_percentage(a):
    total = (a / 100) + 1
    return total


if __name__ == "__main__":

    print("Welcome to the Tip Calculator.")

    print("What was the total bill?")
    bill = float(input())

    print("What percentage tip would you like to give? 10, 12 or 15?")
    tip = int(input())

    print("How many people will split the bill?")
    people = int(input())

    total = round(bill * tip_percentage(tip) / people, 2)
    print(f"Each person should pay: ${total}")
