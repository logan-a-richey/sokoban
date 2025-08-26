# main_window.py

import tkinter as tk

from popups import AboutPopup, WinPopup
from main_canvas import MainCanvas 

class MainWindow(tk.Frame):
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # self.pack() # TODO
        
        self.about_popup = AboutPopup(root, controller) 
        self.win_popup = WinPopup(self, controller) 

        self.canvas = MainCanvas(root, controller)

        self.bind_events()
        self.setup_menubar()
        
    def setup_menubar(self):
        # fetch level data to populate menus
        data : dict = self.controller.level_loader.get_data()
        on_quit : callable = self.controller.on_quit
        on_level_reset : callable = self.controller.on_level_reset
        on_level_load_from_file : callable = self.controller.on_level_load_from_file
        on_levelset_load_from_file : callable = self.controller.on_levelset_load_from_file
        on_level_load : callable = self.controller.load_level

        # setup menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(label="Reset Level [CTRL N]", command=lambda: on_level_reset)
        file_menu.add_command(label="Load Level", command=lambda: on_level_load_from_file)
        file_menu.add_command(label="Load Levelset", command=lambda: on_levelset_load_from_file)
        file_menu.add_command(label="Exit", command=lambda: on_quit() )
        menubar.add_cascade(label="File", menu=file_menu)
        
        # level select

        level_menu = tk.Menu(menubar, tearoff=0)

        num_levels = 0 
        category_name = "null" 
        category_menu = None 

        for levelset in data:
            num_levels = len(levelset)
            for idx, level in enumerate(levelset):
                if (idx % 20 == 0):
                    if category_menu:
                        level_menu.add_cascade(label=category_name, menu=category_menu)

                    # begin a new category
                    lower_idx = idx
                    upper_idx = max(idx + 20, num_levels) - 1
                    category_name = "Levels {} to {}...".format(lower_idx, upper_idx)
                    category_menu = tk.Menu(menu=levels_menu, tearoff=0)
                
                # process the level
                levelname = "Level {}".format(idx)
                category_menu.add_command(
                    label=levelname,
                    command=lambda levelset=levelset, levelname=levelname: on_level_load(levelset, levelname)
                )
        menubar.add_cascade(label="Level Select", menu=level_menu)

        about_menu =  tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Open About", command=lambda: self.about_popup.trigger() )
        menubar.add_cascade(label="About", menu=about_menu)

    def bind_events(self):
        '''
        ctrl n = reset
        ctrl z = undo move
        ctrl y = redo move
        W, A, S, D    = make move
        '''

        self.root.bind("<Escape>", lambda event: self.root.quit() ) 

        pass 

