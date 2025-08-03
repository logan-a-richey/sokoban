#!/usr/bin/env python3

import sys
import json
import tkinter as tk
from tkinter import ttk
from typing import List, Optional

from colors import Colors, convert_hex_to_rgb

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
levelsets = sorted(data.keys())

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

class Grid:
    def __init__(self, i_: int, j_: int):
        self.i = i_
        self.j = j_
        self.is_wall = False
        self.is_player = False
        self.is_block = False
        self.is_place = False

class Level:
    ''' Contains all the level data '''
    def __init__(self, app_: "App", level_string_: str):
        # ref to the game manager in case we want to redraw or update events
        self.app = app_ 

        # store string of original position - should not change this!
        self.level_string = level_string_

        self.grid: List[List["Grid"]] = [] # default to be created
        self.num_rows = 8 # default to be changed
        self.num_cols = 8 # default to be changed
        self.undo_history: List[str] = [] # should contain only chars - see `make_move()`

        # load the level grid
        self.init_grid()
        
    def init_grid(self):
        ''' 
        new game function
        Call this function to reset the level to its initial position 
        '''
        self.undo_history.clear()

        data_lines = self.level_string.split(';')
        print("[DEBUG] data_lines: \n{}", '\n'.join(data_lines))

        # make matrix square in case cols do not match (which is likely)
        self.num_rows = len(data_lines)
        self.num_cols = len(max(data_lines, key=len))

        self.grid = [[Grid(i, j) for j in range(self.num_cols)] for i in range(self.num_rows)]
        for i in range(self.num_rows):
            # NOTE each row may contain different number of cols
            for j, char in enumerate(data_lines[i]):
                g = self.grid[i][j]
                if char == '_':
                    continue # empty
                elif char == '#': 
                    g.is_wall = True
                elif char == '.':
                    g.is_place = True
                elif char == '$':
                    g.is_block = True
                elif char == '*':
                    g.is_block = True
                    g.is_place = True
                elif char == '@':
                    g.is_player = True
                elif char == '+':
                    g.is_player = True
                    g.is_place = True
    
    def get_player_pos(self) -> List[int]:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.grid[i][j].is_player:
                    return [i, j]
        return [-1, -1]

    def make_move(self, move: str):
        px, py = self.get_player_pos()
        
        commands = ['w', 's', 'a', 'd']
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for command, direction in zip(commands, directions):
            if move != command:
                continue
            
            di, dj = direction
            adj1 = [px + di, py + dj]  # Adjacent square in the direction
            adj2 = [px + di * 2, py + dj * 2]  # 2nd adjacent square in the direction

            # NOTE board bounds check
            if (adj1[0] < 0 or adj1[1] < 0 or adj1[0] >= self.num_rows or adj1[1] >= self.num_cols):
                return  # Out of bounds, return without moving

            # Check if player moves into a wall
            if self.grid[adj1[0]][adj1[1]].is_wall:
                return  # Can't move into a wall
            
            # Check if player tries to push a block
            if self.grid[adj1[0]][adj1[1]].is_block:
                # If the next space is free (not a wall or block)
                if (adj2[0] >= 0 and adj2[1] >= 0 and adj2[0] < self.num_rows and adj2[1] < self.num_cols):
                    if not self.grid[adj2[0]][adj2[1]].is_block and not self.grid[adj2[0]][adj2[1]].is_wall:
                        # Push the box to the adjacent space
                        self.grid[adj2[0]][adj2[1]].is_block = True
                        self.grid[adj1[0]][adj1[1]].is_block = False
                        self.grid[px][py].is_player = False
                        self.grid[adj1[0]][adj1[1]].is_player = True
                        return
                # If not, the box can't be pushed
                return

            # Player moves into an empty space
            self.grid[px][py].is_player = False
            self.grid[adj1[0]][adj1[1]].is_player = True
            return
    
    def is_solved(self) -> bool:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                g = self.grid[i][j] 
                if g.is_place and not g.is_block:
                    return False
        return True

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

        # Dropdowns
        self.levelset_menu = ttk.OptionMenu(root, self.levelset_var, self.current_levelset, *self.levelsets, command=self.update_levelset)
        self.level_menu = ttk.OptionMenu(root, self.level_var, self.current_level, *self.levels, command=self.load_level)

        self.levelset_menu.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.level_menu.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.level_obj: Optional["Level"] = None
        self.bind_keys()
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
        self.level_var.set(self.current_level)

        # Update the level dropdown menu
        self.level_menu['menu'].delete(0, 'end')
        for level in self.levels:
            self.level_menu['menu'].add_command(
                label=level, 
                command=tk._setit(self.level_var, level)
            )
        
        # TODO
        self.load_level(self.current_level)

    def load_level(self, selected_level):
        self.current_level = selected_level 
        level_string = data[self.current_levelset][self.current_level]
        
        # TODO this function not being called?
        self.level_obj = Level(self, level_string)

    def draw_board(self):
        if not self.level_obj:
            return 

        self.canvas.delete("all")
        tile_size = 50
        for row in range(self.level_obj.num_rows):
            for col in range(self.level_obj.num_cols):
                g = self.level_obj.grid[row][col]
                color = Colors.TanLight if (row + col) % 2 == 0 else Colors.TanDark
                x0 = col * tile_size
                y0 = row * tile_size
                x1 = x0 + tile_size
                y1 = y0 + tile_size
                hex_color = '#%02x%02x%02x' % color
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=hex_color, outline='black')

    def make_move(self, direction: str):
        if not self.level_obj:
            return

        self.level_obj.make_move(direction)
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = SokobanApp(root)
    root.mainloop()
