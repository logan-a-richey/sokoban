# sokoban_engine.py

from dataclasses import dataclass
from typing import List

@dataclass 
class Tile:
    is_player: bool
    is_wall: bool
    is_block: bool
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

    def new_game(self, level_dict: dict) -> None:
        num_rows = 3 # TODO
        num_cols = 4 # TODO
        self.grid = [[Tile(False, False, False, False) for j in range(num_cols)] for i in range(num_rows)] 
        self.move_history.clear()

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

