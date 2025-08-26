# level_loader.py

import json 

LEVEL_DATA_DIR = "level_data" 

class LevelLoader:
    def __init__(self):
        self.data : dict = {}

    def load_levels(self):
        pass 

    def get_data(self) -> dict:
        return self.data 
