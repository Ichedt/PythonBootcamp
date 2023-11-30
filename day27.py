"""
Day 27 - Distance Converter

tags: tkinter, function arguments
"""
import tkinter


def miles_to_km():
    """Convert input value in miles to kilometers"""

    miles = float(miles_input.get())
    km = round(miles * 1.609)
    kilometer_result_label.config(text=f"{km}")


# Setting up window
window = tkinter.Tk()
window.title("Distance Converter")
window.minsize(width=200, height=100)
window.config(padx=20, pady=20)

# Widgets
miles_input = tkinter.Entry(width=6)
miles_input.grid(column=1, row=0)

miles_label = tkinter.Label(text="miles")
miles_label.grid(column=2, row=0)

equal_to_label = tkinter.Label(text="is equal to")
equal_to_label.grid(column=0, row=1)

kilometer_result_label = tkinter.Label(text="0")
kilometer_result_label.grid(column=1, row=1)

kilometer_label = tkinter.Label(text="km")
kilometer_label.grid(column=2, row=1)

calculate_button = tkinter.Button(text="Calculate", command=miles_to_km)
calculate_button.grid(column=1, row=2)

window.mainloop()
