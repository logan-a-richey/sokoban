# level_loader.py 

import subprocess
import json 

class LevelLoader:
    def __init__(self):
        self.level_data = {}

    def load_levels(self, dir_path):
        pass

    def get_level_data(self):
        return self.level_data = {}
    
    def load_levels_with_perl(self):
        perl_script_path = "./load_levels.pl"
        retcode = subprocess.call(["perl", perl_script_path])
        if retcode == 0:
            print("Levels loaded - ok")
        else:
            print("Levels loaded - FAIL: {}".format(retcode))
            exit(1)

        data = {}
        with open('out.json', 'r') as file:
        data = json.load(file)
        self.level_data = data 

if __name__ == "__main__":

