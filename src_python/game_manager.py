# game_manager.py 

from level_loader import LevelLoader
from progress_manager import ProgressManager
from sokoban_engine import SokobanEngine
from main_window import MainWindow

class GameManager:
    def __init__(self, root):
        # callback to tkinter toplevel
        self.root = root 

        # load levels
        self.level_loader = LevelLoader()
        self.level_loader.load_levels()
        self.data = self.level_loader.get_data()
        
        # persistent memory
        self.progress_manager = ProgressManager()
        
        # core game logic
        self.engine = SokobanEngine()

        # core gui logic
        self.main_window = MainWindow(root, self)
        
        # launch the first level if possible 
        self.load_first_level() 

    def load_first_level(self):
        if not self.data:
            print("No levels to load")
            return

        first_levelset = list(self.data.keys())[0] 
        first_level = list(self.data[first_levelset].keys())[0]
        self.load_level(first_levelset, first_level)
    
    def load_level(self, levelset: str, levelname: str):
        level_data: dict = self.data.get(levelset, {}).get(levelname, "")
        if not level_data:
            print("Failed to load level_data")
            return 
    
    def on_level_load_from_file(self, filepath: str):
        print("Loading level ...")
        pass 

    def on_levelset_load_from_file(self, path: str):
        print("Loading levelsets ...")
        pass

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
        
    def on_zoom_in(self):
        pass

    def on_zoom_out(self):
        pass 

    def on_refresh(self):
        board_state = self.engine.get_board_state()
        self.main_window.canvas.redraw(board_state)

    def on_quit(self):
        self.root.quit()

