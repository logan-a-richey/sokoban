# level.py

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
#   brick.png  player.png  red_sphere.png  white_sphere.png

from typing import List
from colors import Colors 

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
        self.history_index: int = 0

        # load the level grid
        self.init_grid()
        
        self.seen_solved_message = False 

    def init_grid(self):
        ''' 
        new game function
        Call this function to reset the level to its initial position 
        '''

        self.seen_solved_message = False 
        self.undo_history.clear()
        self.history_index = 0

        data_lines = self.level_string.split(';')
        data_lines.pop()

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

    def make_move(self, move: str, truncate=True):
        px, py = self.get_player_pos()

        directions = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if move not in directions: return

        di, dj = directions[move]
        adj1 = [px + di, py + dj]
        adj2 = [px + 2*di, py + 2*dj]

        # Bounds check
        if not (0 <= adj1[0] < self.num_rows and 0 <= adj1[1] < self.num_cols): return

        g1 = self.grid[adj1[0]][adj1[1]]
        g2 = self.grid[adj2[0]][adj2[1]] if (0 <= adj2[0] < self.num_rows and 0 <= adj2[1] < self.num_cols) else None

        move_record = move  # default to lowercase (no push)

        # Wall block
        if g1.is_wall: return

        # Try to push box
        if g1.is_block:
            if g2 and not g2.is_wall and not g2.is_block:
                g2.is_block = True
                g1.is_block = False
                move_record = move.upper()  # Uppercase for push
            else: return  # Can't push

        # Move player
        self.grid[px][py].is_player = False
        g1.is_player = True

        if truncate:
            del self.undo_history[self.history_index:]
            self.undo_history.append(move_record)
        self.history_index += 1

    def undo_move(self):
        if self.history_index == 0:
            print("No more moves to undo!")
            return

        self.history_index -= 1
        action = self.undo_history[self.history_index]
        pi, pj = self.get_player_pos()
        self.grid[pi][pj].is_player = False

        di, dj = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}[action.lower()]
        back_i, back_j = pi - di, pj - dj
        self.grid[back_i][back_j].is_player = True

        if action.isupper():
            # box was pushed — undo it
            box_i, box_j = pi + di, pj + dj
            self.grid[box_i][box_j].is_block = False
            self.grid[pi][pj].is_block = True
    
    def redo_move(self):
        if self.history_index >= len(self.undo_history):
            print("No more moves to redo!")
            return

        move = self.undo_history[self.history_index]
        self.make_move(move.lower(), truncate=False)

    def is_solved(self) -> bool:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                g = self.grid[i][j] 
                if g.is_place and not g.is_block:
                    return False
        return True

