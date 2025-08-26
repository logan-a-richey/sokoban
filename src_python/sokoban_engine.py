# sokoban_engine.py

# '_' empty
# '#' wall
# '.' place 
# '$' box
# '*' box on place 
# '@' player
# '+' player on place
# ';' end of current row 

from dataclasses import dataclass
from typing import List

@dataclass 
class Tile:
    is_player: bool
    is_wall: bool
    is_box: bool
    is_solution_spot: bool

@dataclass 
class BoardState:
    num_rows: int
    num_cols: int 
    grid: List[List["Tile"]]

@dataclass
class SokobanEngine:
    def __init__(self):
        self.grid = []
        self.move_history: List["Move"] = []

    def new_game(self, level_data: str) -> None:
        self.grid.clear()
        self.move_history.clear()
        
        rows = level_data.strip(';').split(';')
        num_rows = len(rows)
        num_cols = 1
        
        for row in rows:
            num_cols = max(num_cols, len(row) )

        self.grid = [ [Tile(False, False, False, False) for j in range(num_cols)] for i in range(num_rows) ] 
        
        for i, row in enumerate(rows):
            for j, char in enumerate(row):
                g = self.grid[i][j]
                if char == '#':
                    g.is_wall = True
                elif char == '.':
                    g.is_solution_spot = True
                elif char == '$':
                    g.is_box = True
                elif char == '*':
                    g.is_box = True
                    g.is_solution_spot = True
                elif char == '@':
                    g.is_player = True
                elif char == '+':
                    g.is_player = True
                    g.is_solution_spot = True
                else:
                    pass
        self.print_grid()
        print()

    def print_grid(self):
        bs = self.get_board_state() 
        for i in range(bs.num_rows):
            for j in range(bs.num_cols):
                g = self.grid[i][j] 
                sym = '.'
                if g.is_wall: 
                    sym = '#'
                elif g.is_player:
                    sym = 'P' if g.is_solution_spot else 'p'
                elif g.is_box:
                    sym = 'B' if g.is_solution_spot else 'b'
                else:
                    sym = '*' if g.is_solution_spot else '.'
                print(sym, end=" ")
            print()
    
    def get_player_pos(self):
        bs = self.get_board_state() 
        for i in range(bs.num_rows):
            for j in range(bs.num_cols):
                g = self.grid[i][j] 
                if g.is_player:
                    return [i, j]
        return [-1, -1]

    def make_move(self, move: str) -> None:
        if move not in ['w', 'a', 's', 'd']:
            return
        
        bs = self.get_board_state()

        directions = {
            'w': [-1, 0], # north
            'a': [0, -1], # west
            's': [1, 0], # south
            'd': [0, 1] # east
        }
        
        # player coords
        pi, pj = self.get_player_pos()
        
        # adjacent grid coords
        direction = directions[move]
        gi = pi + direction[0]
        gj = pj + direction[1]
        
        # bound check
        if (gi < 0 or gi >= bs.num_rows or gj < 0 or gj >= bs.num_cols):
            return
        
        g = bs.grid[gi][gj]
        if g.is_box:
            ai = pi + direction[0] * 2
            aj = pj + direction[1] * 2
            
            # check for border
            if (ai < 0 or ai >= bs.num_rows or aj < 0 or aj >= bs.num_cols):
                return
            
            # check for wall or box collisions
            if self.grid[ai][aj].is_wall or self.grid[ai][aj].is_box:
                return
            
            self.grid[gi][gj].is_box = False 
            self.grid[ai][aj].is_box = True 
        
        # player can move regardless if they are pushing a box
        self.grid[pi][pj].is_player = False
        self.grid[gi][gj].is_player = True

    def redo_move(self) -> None:
        pass

    def undo_move(self) -> None:
        pass

    def is_solved(self) -> bool:
        bs = self.get_board_state() 
        for i in range(bs.num_rows):
            for j in range(bs.num_cols):
                g = self.grid[i][j] 
                if (g.is_solution_spot and not g.is_box):
                    return False
        return True
    
    def get_board_state(self) -> "BoardState":
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])
        return BoardState(num_rows, num_cols, self.grid)

