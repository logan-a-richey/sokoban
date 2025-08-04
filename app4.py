#!/usr/bin/env python3

import re
import sys
import json
from typing import List, Optional

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from colors import Colors, convert_hex_to_rgb
from level import Level

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

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

MIN_TILE_SIZE = 10
MAX_TILE_SIZE = 100

class SokobanApp:
    def __init__(self, root):
        self.root = root
        root.title("Sokoban Game")

        self.tile_size = 40
        self.levelsets: List[str] = sorted(data.keys())
        self.current_levelset: str = self.levelsets[0]

        self.levels: List[str] = sorted(data[self.current_levelset].keys(), key=natural_sort_key)
        self.current_level: str = self.levels[0]

        # --- Combobox variables ---
        self.levelset_var = tk.StringVar(value=self.current_levelset)
        self.level_var = tk.StringVar(value=self.current_level)

        # --- Levelset Combobox ---
        ttk.Label(root, text="Levelset").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.levelset_combo = ttk.Combobox(root, textvariable=self.levelset_var, values=self.levelsets, state="readonly")
        self.levelset_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.levelset_combo.bind("<<ComboboxSelected>>", self.on_levelset_select)

        # --- Level Combobox ---
        ttk.Label(root, text="Level").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.level_combo = ttk.Combobox(root, textvariable=self.level_var, values=self.levels, state="readonly")
        self.level_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.level_combo.bind("<<ComboboxSelected>>", self.on_level_select)

        # --- Control Buttons ---
        self.reset_btn = ttk.Button(root, text="Level Reset", command=self.reset_level)
        self.undo_btn = ttk.Button(root, text="Undo", command=self.undo_move)
        self.redo_btn = ttk.Button(root, text="Redo", command=self.redo_move)
        self.reset_btn.grid(row=2, column=0, padx=5, pady=5)
        self.undo_btn.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.redo_btn.grid(row=2, column=1, padx=5, pady=5, sticky='e')
        
        # --- Images --- 
        self.image_name_to_path = {
            "wall": "assets/brick.png",
            "player": "assets/player.png",
            "box_red": "assets/red_sphere.png",
            "box_white": "assets/white_sphere.png"
        }
        self.pil_images = {}
        self.tk_images = {}
        
        self.load_images()
        self.resize_images()

        # --- Canvas ---
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # --- Game Logic ---
        self.level_obj: Optional["Level"] = None
        self.bind_keys()

        # --- Initial Setup ---
        self.load_level(self.current_level)
    
    def load_images(self):
        for name, path in self.image_name_to_path.items():
            pil_image = Image.open(path)
            self.pil_images[name] = pil_image

    def resize_images(self):
        for name, pil_image in self.pil_images.items():
            pil_image = pil_image.resize( (self.tile_size, self.tile_size), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.tk_images[name] = tk_image

    def bind_keys(self):
        self.root.bind('<w>', lambda event: self.make_move('w'))
        self.root.bind('<s>', lambda event: self.make_move('s'))
        self.root.bind('<a>', lambda event: self.make_move('a'))
        self.root.bind('<d>', lambda event: self.make_move('d'))
        self.root.bind('<Control-equal>', self.zoom_in)
        self.root.bind('<Control-minus>', self.zoom_out)
    
    def zoom_in(self, event=None):
        self.tile_size = min(MAX_TILE_SIZE, self.tile_size + 5)
        self.draw_board()
        print("[ACTION] Zoom in!")

    def zoom_out(self, event=None):
        self.tile_size = max(MIN_TILE_SIZE, self.tile_size - 5)
        self.draw_board()
        print("[ACTION] Zoom out!")

    def on_levelset_select(self, event):
        self.current_levelset = self.levelset_var.get()
        self.levels = sorted(data[self.current_levelset].keys())
        self.current_level = self.levels[0]
        self.level_var.set(self.current_level)
        self.level_combo['values'] = self.levels
        self.load_level(self.current_level)

    def on_level_select(self, event):
        selected_level = self.level_var.get()
        self.load_level(selected_level)

    def load_level(self, selected_level):
        self.current_level = selected_level
        level_string = data[self.current_levelset][self.current_level]
        self.level_obj = Level(self, level_string)

        # self.canvas.config( width=self.tile_size * self.level_obj.num_cols, height=self.tile_size * self.level_obj.num_rows)
        self.draw_board()

    def draw_board(self):
        if not self.level_obj:
            return

        self.canvas.config(
            width=self.tile_size * self.level_obj.num_cols,
            height=self.tile_size * self.level_obj.num_rows
        )
        self.resize_images()

        self.canvas.delete("all")
        for row in range(self.level_obj.num_rows):
            for col in range(self.level_obj.num_cols):
                g = self.level_obj.grid[row][col]
                
                x0 = col * self.tile_size
                y0 = row * self.tile_size
                x1 = x0 + self.tile_size
                y1 = y0 + self.tile_size
                
                if g.is_place:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='#00aa00')
                #elif g.is_wall:
                #    self.canvas.create_rectangle(x0, y0, x1, y1, fill='#000000')
                else:
                    tan_color: str = Colors.TanLight if (row + col) % 2 == 0 else Colors.TanDark
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=tan_color)

                if g.is_block:
                    if g.is_place:
                        self.canvas.create_image(x0, y0, image=self.tk_images['box_white'], anchor='nw')
                    else:
                        self.canvas.create_image(x0, y0, image=self.tk_images['box_red'], anchor='nw')
                if g.is_wall:
                    self.canvas.create_image(x0, y0, image=self.tk_images['wall'], anchor='nw')
                if g.is_player:
                    self.canvas.create_image(x0, y0, image=self.tk_images['player'], anchor='nw')

    def make_move(self, direction: str):
        if not self.level_obj:
            return

        self.level_obj.make_move(direction)
        self.draw_board()

    # --- Button Commands (for now just print) ---
    def reset_level(self):
        print("[ACTION] Reset level")
        if self.level_obj:
            self.level_obj.init_grid()
            self.draw_board()

    def undo_move(self):
        print("[ACTION] Undo move")

    def redo_move(self):
        print("[ACTION] Redo move")

if __name__ == "__main__":
    root = tk.Tk()
    app = SokobanApp(root)
    root.mainloop()

