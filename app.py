import tkinter as tk
from ui.main_window import MainWindow

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TM-Pro")
        MainWindow(self.root)