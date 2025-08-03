#!/usr/bin/env python3

import tkinter as tk
import sys 
import json 

data = {}
with open('out.json', 'r') as file:
    data = json.load(file)

levelsets = sorted(data.keys())
print("levelsets = {}".format(levelsets))
print("data[\'m1\'] = {}".format(sorted(data['m1'].keys())))

exit(0)

def show_selection():
    print("Selected option:", selected_option.get())

# Create the main window
root = tk.Tk()
root.title("Dropdown Menu Example")

# options = ["Option 1", "Option 2", "Option 3", "Option 4"]
options = levelsets

# Create a StringVar to hold the selected option
selected_option = tk.StringVar(root)
selected_option.set(options[0]) # default value

dropdown_menu = tk.OptionMenu(root, selected_option, *options)
dropdown_menu.pack(pady=20)

# Create a button to display the selected value
button = tk.Button(root, text="Show Selection", command=show_selection)
button.pack()

# Run the Tkinter event loop
root.mainloop()


