# object wrapper around a sokoban level 

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

        # load the level grid
        self.init_grid()
        
    def init_grid(self):
        ''' 
        new game function
        Call this function to reset the level to its initial position 
        '''
        self.undo_history.clear()

        data_lines = self.level_string.split(';')
        print("[DEBUG] data_lines:\n{}".format('\n'.join(data_lines)))

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
