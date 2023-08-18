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


def calculator():
    """Calls for the calculation to be done."""
    a = float(input("What is the first number? "))

    for symbol in operations:
        print(symbol)

    should_continue = True

    while should_continue:
        operation = input("Pick an operation: ")
        b = float(input("What is the next number? "))
        calculation = operations[operation]
        result = calculation(a, b)

        print(f"{a} {operation} {b} = {result}")

        if (
            input(
                f"Type 'y' to contiunue calculating with {result}, or type 'c' to start a new calculation: "
            )
            == "y"
        ):
            a = result
        else:
            should_continue = False
            calculator()


calculator()
