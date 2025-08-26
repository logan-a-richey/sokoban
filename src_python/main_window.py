# main_window.py

import re
import tkinter as tk

from popups import AboutPopup, WinPopup
from main_canvas import MainCanvas 

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


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
    
    def build_level_menu(self, menubar, data, on_level_load, levels_per_category=20):
        def natural_sort_key(s):
            import re
            return [int(text) if text.isdigit() else text.lower()
                    for text in re.split("([0-9]+)", s)]

        level_menu = tk.Menu(menubar, tearoff=0)

        for levelset_name in sorted(data.keys(), key=natural_sort_key):
            levelset_menu = tk.Menu(level_menu, tearoff=0)
            num_levels = len(data[levelset_name])

            # iterate through levels
            level_names = list(data[levelset_name].keys())

            levelset_submenu = None
            category_name = None

            for idx, level_name in enumerate(level_names):
                if idx % levels_per_category == 0:
                    # if there's a previous submenu, attach it
                    if levelset_submenu:
                        levelset_menu.add_cascade(label=category_name, menu=levelset_submenu)

                    # make a new submenu
                    levelset_submenu = tk.Menu(levelset_menu, tearoff=0)
                    end_idx = min(idx + levels_per_category - 1, num_levels - 1)
                    category_name = f"Levels {idx + 1} to {end_idx + 1} ..."

                # add the level command
                levelset_submenu.add_command(
                    label=level_name,
                    command=lambda ls=levelset_name, ln=level_name: on_level_load(ls, ln)
                )

            # attach the last submenu
            if levelset_submenu:
                levelset_menu.add_cascade(label=category_name, menu=levelset_submenu)

            # attach this levelset menu
            level_menu.add_cascade(label=levelset_name, menu=levelset_menu)

        menubar.add_cascade(label="Level Select", menu=level_menu)       
    
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
        self.build_level_menu(menubar, data, on_level_load, levels_per_category=20)
        
        # about menu
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

