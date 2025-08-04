#!/usr/bin/env python3

import sys
import json

import tkinter as tk
from tkinter import ttk

from colors import Colors, convert_hex_to_rgb

from typing import List

# --- actual data ---
#data = {}
#with open('out.json', 'r') as file:
#    data = json.load(file)
#levelsets = sorted(data.keys())

# --- symbols ---
# '_' empty
# '#' wall
# '.' place 
# '$' box
# '*' box on place 
# '@' player
# '+' player on place
# ';' end of current row 

# $ ls assets/
# all images are square
# brick.png  player.png  red_sphere.png  white_sphere.png

# Mock data: dict of dicts
data = {
    'm1': {
        'microban_level_1': 'aaa',
        'microban_level_2': 'bbb',
        'microban_level_3': 'ccc'
    },
    'sas1': {
        'sasquatch_level_1': 'ddd',
        'sasquatch_level_2': 'eee',
        'sasquatch_level_3': 'fff'
    },
}

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

        # make matrix square in case cols do not match (which is likely)
        num_rows = len(data_lines)
        num_cols = max(data_lines, key=len)

        self.grid = [[Cell(i, j) for j in range(num_cols)] for i in range(num_rows)]
        for i in range(num_rows):
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
                    g.is_box = True
                elif char == '*':
                    g.is_box = True
                    g.is_spot = True
                elif char == '@':
                    g.is_player = True
                elif char == '+':
                    g.is_player = True
                    g.is_spot = True
    
    def get_player_pos(self) -> List[int, int]:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.grid[i][j].is_player:
                    return [i, j]
        return [-1, -1]

    def make_move(self, move: str):
        # up, down, left right:
        # 'u', 'd', 'l', 'r'
        # 'U', 'D', 'L', 'R' if a block is pushed
        # do nothing if invalid move.
        px, py: List[int, int] = self.get_player_pos()
    
        commands = ['n', 'e', 's', 'w']
        directions = [ (0, 1), (1, 0), (0, -1), (-1, 0) ]
        
        for command, direction in zip(commands, directions):
            if (move != command):
                continue
            
            dx, dy = direction

            adj1 = self.grid[px + dx][py + dy]
            adj2 = self.grid[px + dx * 2][py + dy * 2]
            
            # player tries to move into a wall
            if adj1.is_wall:
                return
            # player tries to push a block
            if adj1.is_block:
                # if vacant space
                if (!adj2.is_block or !adj2.is_wall):
                    adj2.is_block = True
                    self.grid[pp[0]][pp[1]].is_player = False
                    adj1.is_player = True
                    self.move_history.append(command.upper) # uppercase moves that push blocks
                    return
                else:
                    # not a vacant space
                    return 

            # player moves into empty space
            self.grid[pp[0]][pp[1]].is_player = False
            adj1.is_player = True
            self.move_history.append(command)
            return
        return
    
    def is_solved(self) -> bool:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                g = self.grid[i][j] 
                if (g.is_place and !self.is_box):
                    return False
        return True


class SokobanApp:
    def __init__(self, root):
        self.levelsets: List[str] = sorted(data.keys())
        self.current_levelset: str = self.levelsets[0]
        
        # self.levels: List[str] = sorted(data[self.current_levelset].keys())
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
        
        self.draw_board()

    def update_level_list(self):
        self.levels = sorted(data[self.current_levelset].keys())
        self.current_level = self.levels[0]

    def update_levelset(self, x):
        self.current_levelset = x 
        self.update_level_list 
        
        self.level_var.set(self.current_level)

        # Update the level dropdown menu
        self.level_menu['menu'].delete(0, 'end')
        for level in self.levels:
            self.level_menu['menu'].add_command(
                label=level, 
                command=tk._setit(self.level_var, level)
            )
        self.load_level(self, self.current_level)

    def load_level(self, selected_level):
        self.current_level = selected_level 
        
        # NOTE key error?
        level_string = data[self.current_levelset][self.current_level]
        print("levelset = {}, level = {}, leveldata = {}".format(
            self.current_levelset, 
            self.current_level, 
            level_string)
        )

        self.level_obj = Level(self, level_string)

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

