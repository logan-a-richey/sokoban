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


class AboutPopup(AbstractPopup):
    def __init__(self, root, controller):
        super().__init__(root, controller)

    def trigger(self):
        print("AboutPopup Opened")
        pass


class WinPopup(AbstractPopup):
    def __init__(self, root, controller):
        super().__init__(root, controller)

    def trigger(self):
        print("WinPopup Opened")
        pass
