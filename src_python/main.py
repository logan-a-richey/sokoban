#!/usr/bin/env python3 

import tkinter as tk 

from game_manager import GameManager

def main():
    root = tk.Tk()
    root.title("Sokoban App")
    root.geometry("{}x{}".format(800, 800))

    g = GameManager(root)

    root.mainloop()
    
if __name__ == "__main__":
    main()

