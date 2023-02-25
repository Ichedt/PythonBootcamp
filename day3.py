# Day 3 - Treasure Island
#
# tags: conditional statements, logical operators, code blocks, scope

print("Welcome to the Treasure Island!")
print("Your mission is to find the treasure.")
print(
    "As you walk down the path, you encounter a bifurcation. Do you want to go to the [L]eft or [R]ight?")
option1 = input().lower()

if option1 == "l":
    print(
        "You followed the left path and you get stopped by a huge river. Do you want to [S]wim or [W]ait for a boat?")
    option2 = input().lower()

    if option2 == "w":
        print("You waited not long for a boat, as a local was passing by. He kindly takes you to the other side.")
        print(
            "At your final destination in a cave, you encounter three doors. Which door do you choose? [R]ed, [Y]ellow or [B]lue door?")
        option3 = input().lower()

        if option3 == "y":
            print("You found your treasure! Congratulations!")

        else:
            print("You transpass the door you chose and you see a giant lion waiting for his next meal. At least now someone is not hungry anymore.")
    else:
        print("As you jump into the river, you see some alligators. Well... now it's too late.")

else:
    print("You followed the right path and fell into a trap. You ended up getting eaten by local animals.")
