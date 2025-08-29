# setting_manager.py

from dataclasses import dataclass 

@dataclass
class Theme:
    tile_light: str
    tile_dark: str
    tile_solution: str

@dataclass
class SettingsState:
    tile_size: int
    theme: "Theme" 

class SettingsManager:
    def __init__(self):
        self.tile_size = 50 

        self.themes = [] 
        self.current_theme = None 

    def load_themes(self):
        theme1 = Theme("#a0a0a0", "#909090", "#00aa00")
        self.themes.append(theme1)

        self.current_theme = self.themes[0] 

    def on_tile_increase(self):
        self.tile_size = min(100, self.tile_size + 5)

    def on_tile_decrease(self):
        self.tile_size = max(10, self.tile_size - 5)

    def get_state(self) -> "SettingsState":
        return SettingsState(self.tile_size, self.current_theme)

