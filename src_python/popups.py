# popups

import tkinter as tk
from abc import ABC, abstractmethod 

class AbstractPopup(ABC):
    def __init__(self, root, controller):
        self.root = root 
        self.controller = controller

    @abstractmethod
    def trigger(self):
        pass 

    def center_popup(self, popup):
        popup.update_idletasks()
        
        # app dimensions
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()

        # popup dimensions
        popup_w = popup.winfo_width()
        popup_h = popup.winfo_height()
        
        # new popup position
        popup_x = root_x + (root_w // 2) - (popup_w // 2)
        popup_y = root_y + (root_h // 2) - (popup_h // 2)

        popup.geometry("+{}+{}".format(popup_x, popup_y) )


class AboutPopup(AbstractPopup):
    def __init__(self, root, controller):
        super().__init__(root, controller)

    def trigger(self):
        print("AboutPopup Opened")
        popup = tk.Toplevel(self.root)
        popup.title("About Window")
        popup.geometry("500x400")
        
        popup.bind("<Return>", lambda event: popup.destroy() )

        self.center_popup(popup)
        
        label_1 = tk.Label(popup, text="How to play", bg='#777777', font=("Arial", 16))
        label_1.pack(pady=4)

        msg = '\n'.join([
            'This is a clone of the game Sokoban.',
            'The goal is to move all of the spheres to the green tiles.',
            'Move with the WASD keys. The player can push one object at a time.',
            'Spheres already on goal tiles are white, otherwise red.',
            'Try to do it in as few moves possible!'
        ])

        label_2 = tk.Label(popup, text=msg)
        label_2.pack(pady=4)

        label_3 = tk.Label(popup, text="Controls", bg='#777777', font=("Arial", 16))
        label_3.pack(pady=4)

        msg = '\n'.join([
            'WASD   : Movement',
            'CTRL - : Zoom out',
            'CTRL = : Zoom in',
            'CTRL N : Reset puzzle',
            'ESCAPE : Quit program'
        ])
        label_4 = tk.Label(popup, text=msg, font="TkFixedFont", anchor="w", justify="left")
        label_4.pack(pady=4)

        close_button = tk.Button(popup, text="Okay", command=popup.destroy)
        close_button.pack(pady=20)


class WinPopup(AbstractPopup):
    def __init__(self, root, controller):
        super().__init__(root, controller)

    def trigger(self):
        print("WinPopup Opened")
        popup = tk.Toplevel(self.root)
        popup.title("Game over")
        popup.geometry("300x200")
        
        popup.bind("<Return>", lambda event: popup.destroy() )

        self.center_popup(popup)

        msg = '\n'.join([ "You completed the puzzle!", "Congrats!" ])
        label = tk.Label(popup, text=msg).pack(pady=20)
        
        close_button = tk.Button(popup, text="Okay", command=popup.destroy).pack(pady=4)
        
