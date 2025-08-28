# main_canvas.py 

import tkinter as tk

tile_size = 100

class Colors:
    SolutionColor = "#00aa00"
    # TanLight =  "#F0E68C"
    # TanDark  =  "#A07E51"
    TanLight = "#a0a0a0"
    TanDark = "#808080"

class MainCanvas:
    def __init__(self, root, controller):
        self.root = root 
        self.controller = controller 

        self.canvas = tk.Canvas(self.root, bg="#007777")
        self.canvas.pack(side="top", fill="both", expand=True)

        self.canvas.focus_set()
        
        self.tk_images = self.controller.image_handler.tk_images 

    def redraw(self, board_state, setting_state):
        print("on redraw")
        
        tile_size = setting_state.tile_size 

        self.canvas.delete("all")
            
        for row in range(board_state.num_rows):
            for col in range(board_state.num_cols):
                g = board_state.grid[row][col]
                x0 = col * tile_size
                y0 = row * tile_size
                x1 = x0 + tile_size
                y1 = y0 + tile_size
                
                grid_bg_color = "#000000"
                if (g.is_solution_spot):
                    grid_bg_color = "#00aa00"
                elif ((row + col) % 2 == 0):
                    grid_bg_color = "#999999"
                else:
                    grid_bg_color = "#777777"

                self.canvas.create_rectangle( x0, y0, x1, y1, fill=grid_bg_color)

                if g.is_wall:
                    self.canvas.create_image( x0, y0, image=self.tk_images["wall"], anchor="nw")
                
                if g.is_player:
                    self.canvas.create_image( x0, y0, image=self.tk_images["player"], anchor="nw")

                if g.is_box:
                    box_lookup = "box_white" if g.is_solution_spot else "box_red"
                    self.canvas.create_image( x0, y0, image=self.tk_images[box_lookup], anchor="nw")

