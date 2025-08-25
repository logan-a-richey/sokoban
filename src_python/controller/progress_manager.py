# progress_manager.py

import json
import os

class ProgressManager:
    def __init__(self, filename="progress.json"):
        self.filename = filename
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_key(self, levelset, levelname):
        return f"{levelset}_{levelname}"

    def get_info(self, levelset, levelname):
        key = self.get_key(levelset, levelname)
        return self.data.get(key, {"has_solved": False, "minimum_moves": -1})

    def update_progress(self, levelset, levelname, move_count):
        key = self.get_key(levelset, levelname)
        current = self.data.get(key, {"has_solved": False, "minimum_moves": -1})

        if not current["has_solved"] or move_count < current["minimum_moves"]:
            self.data[key] = {
                "has_solved": True,
                "minimum_moves": move_count
            }
            self.save()
