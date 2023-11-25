"""
Day 25 - Brazil States Game

tags: pandas, csv files
"""
import turtle
import pandas

screen = turtle.Screen()
screen.title("Brazil States Game")

# Showing the map
image = "day25/blank_map.gif"
screen.addshape(image)
turtle.shape(image)

# Getting coordinates from the image
# def get_mouse_click_coor(x, y):
#    print(x, y)
# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()

# Pulling the data to an list
data = pandas.read_csv("day25/brazil_states.csv")
all_states = data.state.to_list()

guessed_states = []
while len(guessed_states) < 27:
    # Pop-up window to ask user's state
    answer_state = screen.textinput(
        title=f"{len(guessed_states)}/27 States Correct",
        prompt="What's another state's name?",
    ).title()

    # Generate a csv with the missing states
    if answer_state == "Exit":
        missing_states = [state for state in all_states if state not in guessed_states]
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("day25/states_to_learn.csv")
        break

    # Check user's answers
    if answer_state in all_states:
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        # Get the coordinates
        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(state_data.state.item())

screen.exitonclick()
