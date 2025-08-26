# game_manger.py

from level_loader import LevelLoader
from progress_manager import ProgressManager
from sokoban_engine import SokobanEngine
from main_window import MainWindow

class GameManager:
    def __init__(self, root):
        self.level_loader = LevelLoader()
        self.level_loader.load_levels()
        
        self.progress_manager = ProgressManager()

        # game variables
        self.data = self.level_loader.get_data()
        self.seen_win: bool = False

        self.engine = SokobanEngine()
        self.main_window = MainWindow(root, self)
        
        # start up level
        self.load_first_level()
    
    def load_first_level(self):
        if not self.data:
            print("No levels to load")
            return

        first_levelset = list(self.data.keys())[0] 
        first_level = list(first_levelset.keys())[0].name
        self.load_level(first_levelset, first_level)
    
    def load_level(self, levelset: str, levelname: str):
        level_data: dict = self.data.get(levelset, {}).get(levelname, "")
        if not level_data:
            print("Failed to load level_data")
            return 
    
    def on_make_move(self, move: str):
        print("on_make_move: {}".format(move))
        pass

    def on_redo_move(self):
        print("on_redo_move")
        pass

    def on_undo_move(self):
        print("on_undo_move")
        pass

    def on_level_reset(self):
        print("on_level_reset")
        pass

    def check_is_win(self):
        if self.seen_win:
            return

        if not self.engine.is_solved():
            return

        self.seen_win = True
        self.main_window.win_popup.trigger()
        
        # TODO - progress manager
        return
        

    def on_refresh(self):
        board_state = self.engine.get_board_state()
        self.main_window.canvas.redraw(board_state)



