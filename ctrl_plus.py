#!/usr/bin/env python3

import tkinter as tk

def increase_size(event=None):
    print("Zoom out")

def decrease_size(event=None):
    print("Zoom in!")

root = tk.Tk()
root.title("Ctrl + Plus Example")

# Bind the <Control-plus> event to the increase_size function
root.bind('<Control-equal>', increase_size)
root.bind('<Control-minus>', decrease_size)

label = tk.Label(root, text="Press (CTRL, =) and (CTRL, -) to zoom in and out.")
label.pack(pady=20)

root.mainloop()
