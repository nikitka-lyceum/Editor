from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon, QFontInfo
from PyQt5 import uic

from config import pathAppData, pathBaseTheme, WINDOW_ICON_PATH

import json


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(pathAppData + "settings.ui", self)

        self.set_icons()
        self.set_commands()
        self.load_settings()

    def load_settings(self):
        with open(pathAppData + "settings.json", encoding="utf-8") as sett_file:
            settings = json.loads(sett_file.read())
            self.file_path = settings["file_path"]
            self.file_type = settings["file_type"]
            self.dir_path = settings["dir_path"]
            self.theme = settings["theme"]

    def write_settings(self):
        with open(pathAppData + "settings.json", mode="w", encoding="utf-8") as sett_file:
            data = {
                "file_path": self.file_path,
                "file_type": self.file_type,
                "dir_path": self.dir_path,
                "theme": self.theme
            }
            json.dump(data, sett_file, indent=4)

    def set_icons(self):
        # Window
        self.setWindowIcon(QIcon(WINDOW_ICON_PATH))

    def set_commands(self):
        pass

    def closeEvent(self, a0):
        self.write_settings()
