#!/usr/bin/env python3 
# main.py 

import sys
sys.dont_write_bytecode = True

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

