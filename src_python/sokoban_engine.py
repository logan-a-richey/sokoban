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
        
        print(level_data)
        print(rows)

        num_rows = len(rows)
        num_cols = 1
        
        for row in rows:
            num_cols = max(num_cols, len(row) )

        self.grid = [
            [Tile(False, False, False, False) for j in range(num_cols)] \
            for i in range(num_rows)
        ] 
        
        for i, row in enumerate(rows):
            for j, char in enumerate(row):
                # print(char, end=" ")
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
            # print()

        print("---")
        self.print_grid()
    
    def print_grid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
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

    def make_move(self, move: str) -> None:
        pass

    def redo_move(self) -> None:
        pass

    def undo_move(self) -> None:
        pass

    def is_solved(self) -> bool:
        pass 
    
    def get_board_state(self) -> "BoardState":
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])
        return BoardState(num_rows, num_cols, self.grid)

