#!/usr/bin/env python3

import sys
import json

import tkinter as tk
from tkinter import ttk

from colors import Colors, convert_hex_to_rgb


# load data
#data = {}
#with open('out.json', 'r') as file:
#    data = json.load(file)
#levelsets = sorted(data.keys())

# Mock data: dict of dicts
data = {
    'm1': {
        'microban_level_1': '...',
        'microban_level_2': '...',
        'microban_level_3': '...'
    },
    'sas1': {
        'sasquatch_level_1': '...',
        'sasquatch_level_2': '...',
        'sasquatch_level_3': '...'
    },
}

# Sort levelsets
levelsets = sorted(data.keys())
selected_levelset = levelsets[0]
level_names = sorted(data[selected_levelset].keys())

class SokobanApp:
    def __init__(self, root):
        self.root = root
        root.title("Sokoban Game")

        self.levelset_var = tk.StringVar(value=selected_levelset)
        self.level_var = tk.StringVar(value=level_names[0])

        # Dropdowns
        self.levelset_menu = ttk.OptionMenu(root, self.levelset_var, selected_levelset, *levelsets, command=self.update_levels)
        self.level_menu = ttk.OptionMenu(root, self.level_var, level_names[0], *level_names)

        self.levelset_menu.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.level_menu.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.draw_board()

    def update_levels(self, selected_levelset):
        levels = sorted(data[selected_levelset].keys())
        self.level_var.set(levels[0])

        # Update the level dropdown menu
        self.level_menu['menu'].delete(0, 'end')
        for level in levels:
            self.level_menu['menu'].add_command(
                label=level, 
                command=tk._setit(self.level_var, level)
            )

    def draw_board(self):
        self.canvas.delete("all")
        tile_size = 50
        for row in range(8):
            for col in range(8):
                color = Colors.TanLight if (row + col) % 2 == 0 else Colors.TanDark
                x0 = col * tile_size
                y0 = row * tile_size
                x1 = x0 + tile_size
                y1 = y0 + tile_size
                hex_color = '#%02x%02x%02x' % color
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=hex_color, outline='black')

if __name__ == "__main__":
    root = tk.Tk()
    app = SokobanApp(root)
    root.mainloop()

