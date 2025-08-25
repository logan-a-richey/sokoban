# game_manager_2.py 

from controller.level_loader import LevelLoader 
from controller.progress_manager import ProgressManager
from view.main_window import MainWindow 

PATH_TO_LEVELS = "level_data/"

class GameManager:
    ''' Not functional - rough prototype of code structure '''

    def __init__(self, root):
        self.root = root # tkinter root 

        self.level_loader = LevelLoader()
        self.level_data: dict = self.level_loader.load_levels(PATH_TO_LEVELS)
        
        self.engine = SokobanEngine()
        self.progress_manager = ProgressManager()

        self.main_window = MainWindow(root, self)
    
        self.seen_win: bool = False
        self.last_levelset: str = ""
        self.last_levelname: str = ""

    def on_goto_next_puzzle(self):
        levelset = ""
        levelname = ""
        self.on_new_game(levelset, levelname)

    def on_goto_prev_puzzle(self):
        levelset = ""
        levelname = ""
        self.on_new_game(levelset, levelname)

    def on_new_game(self, levelset: str, levelname: str):
        self.last_levelset = levelset 
        self.levelname = levelname 
        
        this_level_data = self.all_level_data.get(levelset, {}).get(levelname, "")
        if not this_level_data:
            print("Could not retrieve level data {}::{}".format(levelset, levelname))
            exit(1)

        self.engine.new_game(this_level_data) 

    def on_puzzle_reset(self):
        levelset = self.last_levelset
        levelname = self.last_levelname
        self.on_new_game(levelset, levelname)
        pass
    
    def on_move(self, move: str):
        # move should be a char 'w', 'a', 's', or 'd'
        
        # ...

        self.on_check_for_win()
        pass 
    
    def on_undo(self):
        self.engine.undo()
        self.on_refresh()

    def on_redo(self):
        self.engine.redo()
        self.on_refresh()
    
    def on_check_for_win(self):
        if (self.seen_win):
            return

        if (not self.engine.is_solved() ):
            return 

        self.seen_win = True 
        self.main_window.win_popup.trigger() 
        
        # update self.progress_manager

    def on_refresh(self):
        current_board_state = self.engine.get_state()
        self.main_window.refresh(current_board_state)

