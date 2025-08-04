#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Scrollable Listbox with Callback")

listbox_items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10"]

listbox = tk.Listbox(root)
for item in listbox_items:
    listbox.insert(tk.END, item)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

def on_item_selected(event):
    selected_indices = listbox.curselection()
    if selected_indices:
        index = selected_indices[0]
        selected_item = listbox.get(index)
        print(f"Selected: {selected_item} (Index: {index})")

listbox.bind("<<ListboxSelect>>", on_item_selected)

root.mainloop()
