import os
import re

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import uic

from config import pathAppData, pathWindowIcon, allStyles

import json


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(pathAppData + "settings.ui", self)

        self.colors = ""

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.updateWindow)
        self.timer.start()

        self.set_icons()
        self.set_commands()
        self.load_settings(["file_path", "file_type", "dir_path", "theme", "font_family", "python_path"])

    def load_settings(self, toRecord):
        with open(pathAppData + "settings.json", encoding="utf-8") as sett_file:
            settings = json.loads(sett_file.read())
            for item in toRecord:
                exec(f"self.{item} = settings['{item}']")

        self.styleList.clear()
        self.styleList.addItems(allStyles)
        style_index_current = self.styleList.findText(self.theme)
        self.styleList.setCurrentIndex(style_index_current)

        self.fontList.setCurrentFont(QFont(self.font_family))
        self.pythonPath.setText(self.python_path)

    def write_settings(self):
        self.load_settings(["file_type", "file_path", "dir_path"])
        with open(pathAppData + "settings.json", mode="w", encoding="utf-8") as sett_file:
            data = {
                "file_path": self.file_path,
                "file_type": self.file_type,
                "dir_path": self.dir_path,
                "theme": self.theme,
                "font_family": self.font_family,
                "python_path": self.python_path
            }
            json.dump(data, sett_file, indent=4)

    def updateWindow(self):
        self.setStyleSheet(self.colors)
        self.pythonPath.setText(self.python_path)

    def applySettings(self):
        self.theme = self.styleList.currentText()
        self.font_family = self.fontList.currentFont().family()
        self.python_path = self.pythonPath.text()

        # Close Settings Window
        self.close()

    def selectPythonPath(self):
        path = QFileDialog.getOpenFileName(self,
                                           'Select python path',
                                           '',
                                           filter="",
                                           options=QFileDialog.DontUseNativeDialog)[0]

        if not (re.search(r"python*.exe", path.split("/")[-1]) is None):
            self.python_path = path

    def set_icons(self):
        # Window
        self.setWindowIcon(QIcon(pathWindowIcon))

    def set_commands(self):
        self.applyButton.clicked.connect(self.applySettings)
        self.canselButton.clicked.connect(lambda func: self.close())
        self.pythonPath.clicked.connect(self.selectPythonPath)

    def closeEvent(self, a0):
        self.write_settings()
