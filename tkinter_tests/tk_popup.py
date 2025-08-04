#!/usr/bin/env python3

import tkinter as tk

def open_popup():
    popup_window = tk.Toplevel(root)  # Create a Toplevel window, child of 'root'
    popup_window.title("My Popup")
    popup_window.geometry("300x200")

    label = tk.Label(popup_window, text="This is a custom popup window!")
    label.pack(pady=20)

    close_button = tk.Button(popup_window, text="Close", command=popup_window.destroy)
    close_button.pack()

root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")

open_button = tk.Button(root, text="Open Popup", command=open_popup)
open_button.pack(pady=50)

root.mainloop()
