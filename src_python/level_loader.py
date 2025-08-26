# level_loader.py
 
import os
import json 

class LevelLoader:
    def __init__(self, level_dir="level_data"):
        self.level_dir = level_dir
        self.data = {}

    def load_levels(self):
        # iterate over each file in the level_dir
        for file_name in os.listdir(self.level_dir):
            file_path = os.path.join(self.level_dir, file_name)

            # only process regular .txt files
            if not (os.path.isfile(file_path) and file_name.endswith(".txt")):
                continue

            # strip extension to get levelset name
            current_levelset = os.path.splitext(file_name)[0]
            self.data[current_levelset] = {}

            level_count = 0
            level_name = None

            # read file line by line
            with open(file_path, "r") as f:
                for line in f:
                    line = line.replace(' ',  '_')

                    line = line.strip()
                    if not line:
                        continue  # skip blank lines

                    if line.startswith(";"):  # new level
                        level_count += 1
                        level_name = f"Level {level_count}"

                        # look for optional nickname in quotes
                        if "'" in line:
                            nickname = line.split("'", 2)[1]
                            level_name += f" '{nickname}'"

                        # initialize container
                        self.data[current_levelset][level_name] = ""
                        continue

                    # replace whitespace with underscores
                    line = line.replace(" ", "_")
                    if level_name:
                        self.data[current_levelset][level_name] += line + ";"

        print("LevelLoader :: All levels processed.")
        

    def get_data(self) -> dict:
        return self.data

