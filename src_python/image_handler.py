# image_handler.py 

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class ImageHandler:
    def __init__(self):
        self.image_name_to_path = {
            "wall": "assets/brick.png",
            "player": "assets/penguin.png",
            "box_red": "assets/red_sphere.png",
            "box_white": "assets/white_sphere.png"
        }

        self.pil_images = {}
        self.tk_images = {}

        self.load_images()
        self.resize_images(100)

    def load_images(self):
        for name, path in self.image_name_to_path.items():
            pil_image = Image.open(path)
            self.pil_images[name] = pil_image

    def resize_images(self, tile_size: int):
        for name, pil_image in self.pil_images.items():
            pil_image = pil_image.resize( (tile_size, tile_size), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.tk_images[name] = tk_image

