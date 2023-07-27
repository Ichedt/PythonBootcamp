# Day 10 - Calculator
#
# tags: function with output


def add(a, b):
    """Adds a number to the other."""
    return a + b


def sub(a, b):
    """Subtracts a number from the other."""
    return a - b


def mul(a, b):
    """Multiplies a number by the other."""
    return a * b


def div(a, b):
    """Divides a number by the other."""
    return a / b


operations = {"+": add, "-": sub, "*": mul, "/": div}

a = int(input("What is the first number? "))

for symbol in operations:
    print(symbol)
operation = input("Pick an operation from the above: ")

b = int(input("What is the second number? "))

calculation = operations[operation]
result = calculation(a, b)

print(f"{a} {operation} {b} = {result}")
