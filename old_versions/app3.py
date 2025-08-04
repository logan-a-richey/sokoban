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
        self.levelsets: List[str] = sorted(data.keys())
        self.current_levelset: str = self.levelsets[0]
        
        self.levels: List[str] = []
        self.current_level: str = ""
        self.update_level_list()

        self.root = root
        root.title("Sokoban Game")
        
        self.levelset_var = tk.StringVar(value=self.current_levelset)
        self.level_var = tk.StringVar(value=self.current_level)
        
        # TODO - old version with dropdown
        # Dropdowns
        self.levelset_menu = ttk.OptionMenu(root, self.levelset_var, self.current_levelset, *self.levelsets, command=self.update_levelset)
        self.level_menu = ttk.OptionMenu(root, self.level_var, self.current_level, *self.levels, command=self.load_level)
        self.levelset_menu.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.level_menu.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # TODO - new version with listbox
        # self.level_listbox = tk.Listbox(root, height=10, exportselection=False)
        # self.level_scrollbar = tk.Scrollbar(root, orient="vertical", command=self.level_listbox.yview)
        # self.level_listbox.config(yscrollcommand=self.level_scrollbar.set)
        # self.level_listbox.grid(row=0, column=1, padx=5, pady=5, sticky='ns')
        # self.level_scrollbar.grid(row=0, column=2, sticky='ns')
        # self.level_listbox.bind('<<ListboxSelect>>', self.on_level_select)


        # Canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.level_obj: Optional["Level"] = None
        self.bind_keys()

        self.tile_size = 40
        self.draw_board()

    def bind_keys(self):
        self.root.bind('<w>', lambda event: self.make_move('w'))
        self.root.bind('<s>', lambda event: self.make_move('s'))
        self.root.bind('<a>', lambda event: self.make_move('a'))
        self.root.bind('<d>', lambda event: self.make_move('d'))

    def update_level_list(self):
        self.levels = sorted(data[self.current_levelset].keys())
        self.current_level = self.levels[0]

    def update_levelset(self, x):
        self.current_levelset = x 
        self.update_level_list()

        self.level_listbox.delete(0, tk.END)
        for level in self.levels:
            self.level_listbox.insert(tk.END, level)

        self.current_level = self.levels[0]
        self.level_listbox.selection_set(0)
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
        selection = event.widget.curselection()
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
                
                x0 = col * self.tile_size
                y0 = row * self.tile_size
                x1 = x0 + self.tile_size
                y1 = y0 + self.tile_size
                
                tan_color = Colors.TanLight if (row + col) % 2 == 0 else Colors.TanDark
                # hex_color = '#%02x%02x%02x' % color
                
                if g.is_place:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='#00aa00')
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=tan_color)

                if g.is_block:
                    if g.is_place:
                        pass # draw white sphere
                    else:
                        pass # draw red sphere

                if g.is_wall:
                    pass # draw wall
                
                if g.is_player:
                    pass # draw player

    def make_move(self, direction: str):
        if not self.level_obj:
            return

        self.level_obj.make_move(direction)
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = SokobanApp(root)
    root.mainloop()
