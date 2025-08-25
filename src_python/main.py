#!/usr/bin/env python3 

from controller.game_manager import GameManager

def main():
    root = tk.Tk()
    g = GameManager(root)
    root.mainloop()
    return 

if __name__ == "__main__":
    main()

