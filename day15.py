"""
Day 15 - Coffee Machine Project

Description: This is a simulation of a coffee machine, which includes three flavours, their ingredients and their price. The coffee machine has its own resources that need to be managed in order to produce the coffees. Also, the machine is operated by coins. As requirements, the machine must report its resources and warn the user when there's not enough resources to produce the coffee.
"""

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0
    }
}

profit = 0

def is_resource_sufficient(order_ingredients):
    """Checks if the ingredients of the order are available and returns True or False."""
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"Sorry, there's not enough {item}")
            return False
    return True


def process_coins():
    "Asks for the coins and returns the total amount."
    print("Please insert coins.")
    total = int(input("How many quarters? ")) * 0.25
    total += int(input("How many dimes? ")) * 0.1
    total += int(input("How many nickles? ")) * 0.05
    total += int(input("How many pennies? ")) * 0.01
    return total


def is_transaction_successful(money_received, drink_cost):
    """Checks if the amount inserted is enough for the drink ordered and returns True or False."""
    if money_received >= drink_cost:
        global profit
        profit += drink_cost
        change = round(money_received - drink_cost, 2)
        print(f"Here's your ${change} change.")
        return True
    else:
        print("Sorry, that's not enough money.")
        return False


def make_coffee(drink_name, order_ingredients):
    """Updates the resourses based on the order."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {drink_name} ☕")


resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


is_on = True

while is_on:
    choice = input("What would you like? (espresso/latte/cappuccino): ")

    # To turn off the machine
    if choice == "off":
        is_on = False
    # To show the resources
    elif choice == "report":
        print(f"Water: {resources["water"]} g")
        print(f"Milk: {resources["milk"]} g")
        print(f"Coffee: {resources["coffee"]} g")
        print(f"Money: ${profit}")
    # To make the drink
    else:
        drink = MENU[choice]
        if is_resource_sufficient(drink["ingredients"]):
            payment = process_coins()
            if is_transaction_successful(payment, drink["cost"]):
                make_coffee(choice, drink["ingredients"])
