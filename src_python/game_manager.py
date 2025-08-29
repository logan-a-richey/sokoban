# game_manager.py 

from level_loader import LevelLoader
from progress_manager import ProgressManager
from settings_manager import SettingsManager
from sokoban_engine import SokobanEngine
from image_handler import ImageHandler
from main_window import MainWindow

class GameManager:
    def __init__(self, root):
        # callback to tkinter toplevel
        self.root = root 

        # core game logic
        self.engine = SokobanEngine()
        
        # persistent memory
        self.progress_manager = ProgressManager()
        self.settings_manager = SettingsManager() 
        self.image_handler = ImageHandler()
        
        # load levels
        self.level_loader = LevelLoader()
        self.level_loader.load_levels()
        self.data = self.level_loader.get_data()
        
        self.last_levelname = ""
        self.last_levelset = ""

        # core gui logic
        self.main_window = MainWindow(root, self)
        
        # launch the first level if possible 
        self.seen_win = False
        self.load_first_level() 

    # level load functions --------------------------------------------------
    def load_first_level(self):
        if not self.data:
            print("No levels to load")
            return

        # first_levelset = list(self.data.keys())[0] 
        first_levelset = "Microban1"
        first_level = list(self.data[first_levelset].keys())[0]
        self.load_level(first_levelset, first_level)
    
    def load_level(self, levelset: str, levelname: str):
        level_data: dict = self.data.get(levelset, {}).get(levelname, "")
        
        if not level_data:
            print("Failed to load level_data")
            return 
        
        print("Loaded levelset \'{}\' level \'{}\'".format(levelset, levelname))
        self.engine.new_game(level_data)
        self.on_refresh()

    def  on_level_reload(self):
        print("on_level_reset")
        self.load_level(self.last_levelset, self.last_levelname)
    
    # TODO
    def on_level_import(self, filepath: str):
        print("Loading level ...")
        pass 
    
    # TODO
    def on_levelset_import(self, path: str):
        print("Loading levelsets ...")
        pass
    
    # engine move functions --------------------------------------------------
    def on_make_move(self, move: str):
        print("on_make_move: {}".format(move))
        self.engine.make_move(move)
        self.on_refresh()
        self.check_is_win()

    def on_redo_move(self):
        print("on_redo_move")
        self.engine.redo_move()
        self.on_refresh()

    def on_undo_move(self):
        print("on_undo_move")
        self.engine.undo_move()
        self.on_refresh()

    def check_is_win(self):
        if self.seen_win:
            return

        if not self.engine.is_solved():
            return

        self.seen_win = True
        self.main_window.win_popup.trigger()
        
        # TODO - progress manager
        pass

    # ui functions  --------------------------------------------------
    def on_zoom_in(self):
        print("on_zoom_in")
        self.settings_manager.on_tile_increase()
        self.on_refresh()

    def on_zoom_out(self):
        print("on_zoom_out")
        self.settings_manager.on_tile_decrease()
        self.on_refresh()

    def on_refresh(self):
        board_state = self.engine.get_board_state()
        setting_state = self.settings_manager.get_state()
        self.image_handler.resize_images(setting_state.tile_size)
        self.main_window.canvas.redraw(board_state, setting_state)

    def on_quit(self):
        self.root.quit()

