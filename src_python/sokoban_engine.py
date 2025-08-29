# sokoban_engine.py

# '_' empty
# '#' wall
# '.' place 
# '$' box
# '*' box on place 
# '@' player
# '+' player on place
# ';' end of current row 

# TODO 
# a move that doesn't push a block is lowercase wasd
# a move that does push a block is uppercase WASD

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
class Move:
    direction: str
    pushed: bool 

@dataclass
class SokobanEngine:
    def __init__(self):
        self.grid: List[List["Tile"]] = []
        self.move_history: List["Move"] = []
        self.move_idx: int = 0 

    def new_game(self, level_data: str) -> None:
        self.grid.clear()
        self.move_history.clear()
        self.move_idx = 0 

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
    
    def make_move(self, move: str, truncate=True):
        px, py = self.get_player_pos()

        directions = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if move.lower() not in directions:
            return

        di, dj = directions[move.lower()]
        adj1 = [px + di, py + dj]
        adj2 = [px + 2*di, py + 2*dj]

        # Bounds check
        if not (0 <= adj1[0] < len(self.grid) and 0 <= adj1[1] < len(self.grid[0])):
            return

        g1 = self.grid[adj1[0]][adj1[1]]
        g2 = self.grid[adj2[0]][adj2[1]] if (0 <= adj2[0] < len(self.grid) and 0 <= adj2[1] < len(self.grid[0])) else None

        pushed = False

        if g1.is_wall:
            return

        if g1.is_box:
            if g2 and not g2.is_wall and not g2.is_box:
                g2.is_box = True
                g1.is_box = False
                pushed = True
            else:
                return

        # Move player
        self.grid[px][py].is_player = False
        g1.is_player = True

        # Only record if this is a new move
        if truncate:
            # Remove future redo moves
            del self.move_history[self.move_idx:]
            self.move_history.append(Move(move.lower(), pushed))
            self.move_idx += 1

    def undo_move(self):
        if self.move_idx == 0:
            return

        self.move_idx -= 1
        last_move = self.move_history[self.move_idx]

        pi, pj = self.get_player_pos()
        self.grid[pi][pj].is_player = False

        directions = {'w': (-1,0), 's': (1,0), 'a': (0,-1), 'd': (0,1)}
        di, dj = directions[last_move.direction]

        # Player moves back
        back_i, back_j = pi - di, pj - dj
        self.grid[back_i][back_j].is_player = True

        if last_move.pushed:
            # Move box back
            box_i, box_j = pi + di, pj + dj
            self.grid[box_i][box_j].is_box = False
            self.grid[pi][pj].is_box = True

    def redo_move(self):
        if self.move_idx >= len(self.move_history):
            return

        move = self.move_history[self.move_idx]
        # replay move without recording again
        self.make_move(move.direction, truncate=False)
        self.move_idx += 1

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

