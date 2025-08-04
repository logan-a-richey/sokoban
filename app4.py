#!/usr/bin/env python3

import sys
import json
import tkinter as tk
from tkinter import ttk
from typing import List, Optional

from colors import Colors, convert_hex_to_rgb
from level import Level

# NOTE
# --- symbols ---
# '_' empty
# '#' wall
# '.' place 
# '$' box
# '*' box on place 
# '@' player
# '+' player on place
# ';' end of current row 

# TODO
# $ ls assets/
# all images are square
# brick.png  player.png  red_sphere.png  white_sphere.png

# --- actual data ---
data = {}
with open('out.json', 'r') as file:
    data = json.load(file)

# Mock data: dict of dicts
#data = {
#    'm1': {
#        'microban_level_1': 'aaa',
#        'microban_level_2': 'bbb',
#        'microban_level_3': 'ccc'
#    },
#    'sas1': {
#        'sasquatch_level_1': 'ddd',
#        'sasquatch_level_2': 'eee',
#        'sasquatch_level_3': 'fff'
#    },
#}

class SokobanApp:
    def __init__(self, root):
        self.root = root
        root.title("Sokoban Game")

        self.tile_size = 40
        self.levelsets: List[str] = sorted(data.keys())
        self.current_levelset: str = self.levelsets[0]

        self.levels: List[str] = sorted(data[self.current_levelset].keys())
        self.current_level: str = self.levels[0]

        # --- UI Variables ---
        self.levelset_var = tk.StringVar(value=self.current_levelset)

        # --- Levelset Dropdown ---
        self.levelset_menu = ttk.OptionMenu(
            root,
            self.levelset_var,
            self.current_levelset,
            *self.levelsets,
            command=self.update_levelset
        )
        self.levelset_menu.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # --- Level Scrollbox ---
        self.level_listbox = tk.Listbox(root, height=10, exportselection=False)
        self.level_scrollbar = tk.Scrollbar(root, orient="vertical", command=self.level_listbox.yview)
        self.level_listbox.config(yscrollcommand=self.level_scrollbar.set)
        self.level_listbox.grid(row=0, column=1, padx=5, pady=5, sticky='ns')
        self.level_scrollbar.grid(row=0, column=2, sticky='ns')
        self.level_listbox.bind('<<ListboxSelect>>', self.on_level_select)

        # --- Canvas ---
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # --- Game Logic ---
        self.level_obj: Optional["Level"] = None
        self.bind_keys()

        # --- Initial Setup ---
        self.populate_level_listbox()
        self.load_level(self.current_level)

    def bind_keys(self):
        self.root.bind('<w>', lambda event: self.make_move('w'))
        self.root.bind('<s>', lambda event: self.make_move('s'))
        self.root.bind('<a>', lambda event: self.make_move('a'))
        self.root.bind('<d>', lambda event: self.make_move('d'))

    def populate_level_listbox(self):
        self.level_listbox.delete(0, tk.END)
        for level in self.levels:
            self.level_listbox.insert(tk.END, level)
        self.level_listbox.selection_set(0)

    def update_levelset(self, new_levelset):
        self.current_levelset = new_levelset
        self.levels = sorted(data[self.current_levelset].keys())
        self.current_level = self.levels[0]

        self.populate_level_listbox()
        self.load_level(self.current_level)

    def load_level(self, selected_level):
        self.current_level = selected_level
        level_string = data[self.current_levelset][self.current_level]
        self.level_obj = Level(self, level_string)

        self.canvas.config(
            width=self.tile_size * self.level_obj.num_cols,
            height=self.tile_size * self.level_obj.num_rows
        )
        self.draw_board()

    def on_level_select(self, event):
        selection = self.level_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.current_level = self.levels[index]
        self.load_level(self.current_level)

    def draw_board(self):
        if not self.level_obj:
            return

        self.canvas.delete("all")
        for row in range(self.level_obj.num_rows):
            for col in range(self.level_obj.num_cols):
                g = self.level_obj.grid[row][col]
                tan_color = Colors.TanLight if (row + col) % 2 == 0 else Colors.TanDark
                x0 = col * self.tile_size
                y0 = row * self.tile_size
                x1 = x0 + self.tile_size
                y1 = y0 + self.tile_size

                if g.is_place:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='#00aa00')
                elif g.is_wall:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='#000000')
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=tan_color)

                # Placeholder: sprite rendering will go here
                if g.is_block:
                    pass  # TODO: draw red/white sphere
                if g.is_wall:
                    pass  # TODO: draw wall tile
                if g.is_player:
                    pass  # TODO: draw player sprite

    def make_move(self, direction: str):
        if not self.level_obj:
            return

        self.level_obj.make_move(direction)
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = SokobanApp(root)
    root.mainloop()
