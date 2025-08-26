# main_canvas.py 

import tkinter as tk

class MainCanvas:
    def __init__(self, root, controller):
        self.root = root 
        self.controller = controller 

        self.canvas = tk.Canvas()

    def redraw(self, board_state):
        # clear canvas
        self.canvas.delete("all")

