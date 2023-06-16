# Day 9 - Auction Program
#
# tags: dictionary, nesting
import os


def highest_bid(bids):
    highest = 0
    winner = ""

    for bidder in bids:
        bid_amount = bids[bidder]

        if bid_amount > highest:
            highest = bid_amount
            winner = bidder

    print(f"The winner is {winner} with a bid of ${highest}")


if __name__ == "__main__":
    option = True
    bids = {}

    while option:
        name = input("What is your name? ")
        price = int(input("What is your bid? $"))
        bids[name] = price

        option = input("Are there other bidders? Type 'yes' or 'no'.\n")
        if option == "yes":
            # Command for clearing the terminal
            os.system("cls")
            pass
        elif option == "no":
            option = False
        else:
            print("Invalid option. Exiting...")

    highest_bid(bids)
