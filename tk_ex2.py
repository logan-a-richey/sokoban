#!/usr/bin/env python3

import tkinter as tk

def update_second_menu(event=None):
    """Updates the options of the second OptionMenu based on the first's selection."""
    selected_category = category_var.get()
    
    # Define options for the second menu based on the selected category
    if selected_category == "Fruits":
        new_options = ["Apple", "Banana", "Orange"]
    elif selected_category == "Vegetables":
        new_options = ["Carrot", "Spinach", "Broccoli"]
    else:
        new_options = ["Select an item"]

    # Clear existing options in the second OptionMenu
    item_menu["menu"].delete(0, "end")

    # Add new options to the second OptionMenu
    for option in new_options:
        item_menu["menu"].add_command(label=option, command=tk._setit(item_var, option))

root = tk.Tk()
root.title("Dynamic Menus")

# First OptionMenu (Category)
category_var = tk.StringVar(root)
category_var.set("Select Category")
categories = ["Fruits", "Vegetables"]
category_menu = tk.OptionMenu(root, category_var, *categories)
category_menu.pack(pady=10)

# Link the callback to the category_var
category_var.trace_add("write", update_second_menu)

# Second OptionMenu (Items)
item_var = tk.StringVar(root)
item_var.set("Select an item")
item_menu = tk.OptionMenu(root, item_var, "Select an item") # Initial placeholder
item_menu.pack(pady=10)

root.mainloop()
