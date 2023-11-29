"""
Day 27 - Distance Converter

tags: graphical user interface, tkinter, function arguments
"""
import tkinter

window = tkinter.Tk()
window.title("GUI Program")
window.minsize(width=500, height=300)

# Label
my_label = tkinter.Label(text="I'm a label", font=("Arial", 24, "normal"))
my_label.pack()

window.mainloop()
