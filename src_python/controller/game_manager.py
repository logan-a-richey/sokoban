#!/usr/bin/env python3

import re
import sys
import json
from typing import List, Optional

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from colors import Colors, convert_hex_to_rgb
from level import Level
from progress_manager import ProgressManager 

from controller.level_loader import LevelLoader 

# --- actual data ---
import subprocess

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

MIN_TILE_SIZE = 10
MAX_TILE_SIZE = 100

class MainWindow:
    def __init__(self, root):
        print("Running SokobanApp!")

        self.root = root
        root.title("Sokoban Game")
        
        self.progress_manager = ProgressManager()

        self.tile_size = 40
        self.levelsets: List[str] = sorted(data.keys(), key=natural_sort_key)
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
            "player": "assets/penguin.png",
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
        self.populate_level_combobox()
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
        # lower move
        self.root.bind('<w>', lambda event: self.make_move('w'))
        self.root.bind('<s>', lambda event: self.make_move('s'))
        self.root.bind('<a>', lambda event: self.make_move('a'))
        self.root.bind('<d>', lambda event: self.make_move('d'))
        
        # upper move
        self.root.bind('<W>', lambda event: self.make_move('w', repeat=5))
        self.root.bind('<S>', lambda event: self.make_move('s', repeat=5))
        self.root.bind('<A>', lambda event: self.make_move('a', repeat=5))
        self.root.bind('<D>', lambda event: self.make_move('d', repeat=5))

        # zoom
        self.root.bind('<Control-equal>', self.zoom_in)
        self.root.bind('<Control-minus>', self.zoom_out)

        # level events
        self.root.bind('<Control-n>', self.reset_level)
        self.root.bind('<Control-z>', self.undo_move)
        self.root.bind('<Control-y>', self.redo_move)
    
    def zoom_in(self, event=None):
        self.tile_size = min(MAX_TILE_SIZE, self.tile_size + 5)
        self.draw_board()
        print("[ACTION] Zoom in!")

    def zoom_out(self, event=None):
        self.tile_size = max(MIN_TILE_SIZE, self.tile_size - 5)
        self.draw_board()
        print("[ACTION] Zoom out!")
    
    def populate_level_combobox(self):
        values = []

        for lvl in self.levels:
            info = self.progress_manager.get_info(self.current_levelset, lvl)
            status = "[X]" if info["has_solved"] else "[ ]"
            move_str = f" ({info['minimum_moves']}m)" if info["minimum_moves"] != -1 else ""
            display_label = f"{status} {lvl}{move_str}"
            values.append(display_label)

        self.level_combo['values'] = values

    def on_levelset_select(self, event):
        self.current_levelset = self.levelset_var.get()
        self.levels = sorted(data[self.current_levelset].keys(), key=natural_sort_key)
        self.current_level = self.levels[0]
        self.level_var.set(self.current_level)
        self.load_level(self.current_level)
        
        # self.level_combo['values'] = self.levels
        self.populate_level_combobox()

    def on_level_select(self, event):
        # TODO 
        # selected_level = self.level_var.get()
        # self.load_level(selected_level)

        # NOTE strip [X] [ ] prefix from a level name
        label = self.level_var.get()
        match = re.search(r"\] (.+?)(?: \(\d+m\))?$", label)
        level_name = match.group(1) if match else label
        self.load_level(level_name)

    def load_level(self, selected_level):
        self.current_level = selected_level
        level_string = data[self.current_levelset][self.current_level]
        self.level_obj = Level(self, level_string)
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

    def make_move(self, direction: str, repeat=1):
        if not self.level_obj:
            return
        
        for i in range(repeat):
            self.level_obj.make_move(direction)
            self.draw_board()

        # Alert when solved
        if(self.level_obj.is_solved()):
            if self.level_obj.seen_solved_message:
                return
            
            self.level_obj.seen_solved_message = True  
            
            num_moves = len(self.level_obj.undo_history)
            
            self.progress_manager.update_progress(self.current_levelset, self.current_level, num_moves)
            self.populate_level_combobox()
            
            self.spawn_level_win_popup()

    def spawn_level_win_popup(self):
        popup_window = tk.Toplevel(self.root)
        popup_window.title("Level completed.")
        popup_window.geometry("300x200")
       
        num_moves = len(self.level_obj.undo_history)
        
        message = "Congrats!\nSolved \'{} {}\' in {} moves.".format(
            self.current_levelset, 
            self.current_level, 
            num_moves
        )

        label = tk.Label(popup_window, text=message)
        label.pack(pady=20)
        
        def next_level_button_func():
            print("call next level button")
            this_level_index = self.levels.index(self.current_level)
            next_level_index = (this_level_index + 1) % len(self.levels)
            self.on_level_select(self.levels[next_level_index])
            popup_window.destroy()
            return 

        next_level_button = tk.Button(popup_window, text="Next Level", command=next_level_button_func)
        next_level_button.pack()
        
        close_button = tk.Button(popup_window, text="Close", command=popup_window.destroy)
        close_button.pack()
        
        # TODO 
        pass 

    # --- Button Commands (for now just print) ---
    def reset_level(self, event=None):
        # print("[ACTION] Reset level")
        if not self.level_obj:
            return

        self.level_obj.init_grid()
        self.draw_board()

    def undo_move(self, event=None):
        # print("[ACTION] Undo move")
        if not self.level_obj:
            return

        self.level_obj.undo_move()
        self.draw_board()

    def redo_move(self, event=None):
        # print("[ACTION] Redo move")
        if not self.level_obj:
            return

        self.level_obj.redo_move()
        self.draw_board()

