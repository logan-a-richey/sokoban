# main_window.py

import tkinter as tk

from main_canvas import MainCanvas 

class MainWindow(tk.Frame):
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # self.pack() # TODO
        
        self.canvas = MainCanvas(root, controller)

        self.bind_events()
        self.setup_menubar()
        
    def setup_menubar(self):
        pass
    
    def bind_events(self):
        '''
        ctrl n = reset
        ctrl z = undo move
        ctrl y = redo move
        W, A, S, D    = make move
        '''
        pass 

