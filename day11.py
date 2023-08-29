# Day 11 - Blackjack Game
#
# tags: functions, recursion
import random
import os


def clear_console():
    """Clears the console log."""
    os.system("cls")


def deal_card():
    """Returns a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(cards)
    return card


def calculate_score(cards):
    """Takes a list of cards and calculates the score from the cards."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0

    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)

    return sum(cards)


def compare(user_score, dealer_score):
    """Compares two scores and decides the winner."""
    if user_score == dealer_score:
        return "Draw!"
    elif dealer_score == 0:
        return "Lose, opponent has Blackjack."
    elif user_score == 0:
        return "Win with a Blackjack!"
    elif user_score > 21:
        return "You went over. You lose!"
    elif dealer_score > 21:
        return "Opponent went over. You win!"
    elif user_score > dealer_score:
        return "You win!"
    else:
        return "You lose!"


def play_game():
    user_cards = []
    dealer_cards = []
    is_game_over = False

    for _ in range(2):
        user_cards.append(deal_card())
        dealer_cards.append(deal_card())

    while not is_game_over:
        user_score = calculate_score(user_cards)
        dealer_score = calculate_score(dealer_cards)

        if user_score == 0 or dealer_score == 0 or user_score > 21:
            is_game_over = True
        else:
            user_should_deal = input('Type "y" to get another card, type "n" to pass: ')
            if user_should_deal == "y":
                user_cards.append(deal_card())
            else:
                is_game_over = True

    while dealer_score != 0 and dealer_score < 17:
        dealer_cards.append(deal_card())
        dealer_score = calculate_score(dealer_cards)

    print(f"    Your final hand: {user_cards}, final score: {user_score}")
    print(f"    Dealer1s final hand: {dealer_cards}, final score: {dealer_score}")
    print(compare(user_score, dealer_score))


while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == "y":
    clear_console()
    play_game()
