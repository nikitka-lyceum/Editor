import json
import os
import sqlite3
import subprocess
import time

from PyQt5.QtCore import QTimer, QPoint, QThread, QProcess
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QTextEdit, QTabWidget, QMenuBar, QMenu, QAction, \
    QHBoxLayout, QPushButton, QLabel, QWidget, QDialog
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5 import uic, QtWidgets, QtCore, QtGui

from appData.ui.editorUi import Ui_Editor
from config import pathAppData, pathBase, pathIcons, allEncodings

from classes.Highlighter import Highlighter
from classes.Settings import Settings


class EditorCode(QMainWindow, Ui_Editor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.settApp = Settings()

        self.file_path = ""
        self.file_type = ""
        self.dir_path = ""
        self.theme = "standard"
        self.font_family = ""
        self.python_path = ""
        self.encoding = ""

        # Update
        self.updater = QTimer()
        self.updater.setInterval(1000)
        self.updater.timeout.connect(self.updateWindow)
        self.updater.start()

        # Set Console Settings
        self.consolesTab.removeTab(1)
        self.consolesTab.setFixedHeight(250)

        # Set Code Edit Settings
        self.codeEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.codeEdit.setStyleSheet("selection-background-color: #8F4C61")

        # Set Widget Settings
        try:
            self.set_icons()
            self.set_commands()
            self.load_settings(
                ["file_path", "file_type", "dir_path", "theme", "font_family", "python_path", "encoding"])
            self.open_file()
            self.open_folder()
            self.connectBase()
        except Exception as e:
            print(e)

    def connectBase(self):
        # Open Base Colors
        self.con_color = sqlite3.connect(pathBase + "theme.sqlite", check_same_thread=False)
        self.cur_color = self.con_color.cursor()
        self.cur_color.execute("""CREATE TABLE IF NOT EXISTS code_themes(
                    file_type TEXT,
                    name TEXT,
                    colors TEXT
                )""")

        self.cur_color.execute("""CREATE TABLE IF NOT EXISTS widget_themes(
                    name TEXT,
                    colors TEXT
                )""")

        # Open Base Control Points
        self.con_control_point = sqlite3.connect(pathBase + "controlPoint.sqlite", check_same_thread=False)
        self.cur_control_point = self.con_control_point.cursor()
        self.cur_control_point.execute("""CREATE TABLE IF NOT EXISTS points(
                            file_type TEXT,
                            file_path TEXT,
                            code TEXT
                        )""")

    def selectFile(self, index):
        path = self.sender().model().filePath(index)
        if os.path.isfile(path):
            self.file_path = path
            self.file_type = os.path.splitext(self.file_path)[-1]
            self.open_file()

    def create_file(self):
        if self.sender().text() == "Python File":
            name, ok_pressed = QInputDialog().getText(self, "New Python file", "")
            if ".py" not in name[-3:]:
                self.file_type = ".py"
                name += ".py"

        elif self.sender().text() == "Other File":
            name, ok_pressed = QInputDialog().getText(self, "New File", "")

        else:
            ok_pressed = False

        if ok_pressed:
            self.file_path = os.getcwd().strip() + "\\" + name

            with open(self.file_path, mode="w+", encoding=self.encoding):
                pass

            self.codeEdit.clear()

    def save_file(self):
        try:
            if self.sender().text() == "Save" and self.file_path == "":
                self.file_path, self.file_type = QFileDialog.getSaveFileName(self,
                                                                             "Save as",
                                                                             options=QFileDialog.DontUseNativeDialog
                                                                             )
        except Exception:
            pass

        if os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding=self.encoding) as save_file:
                save_file.write(self.codeEdit.toPlainText())

    def open_file(self):
        if not (self.sender() is None):
            if self.sender().text() == "Python File":
                self.file_path, self.file_type = QFileDialog.getOpenFileName(self,
                                                                             'Select python file',
                                                                             '',
                                                                             filter="*.py",
                                                                             options=QFileDialog.DontUseNativeDialog)

            elif self.sender().text() == "File":
                self.file_path, self.file_type = QFileDialog.getOpenFileName(self,
                                                                             'Select File',
                                                                             '',
                                                                             options=QFileDialog.DontUseNativeDialog)

        if os.path.exists(self.file_path):
            with open(self.file_path, mode="r", encoding=self.encoding) as open_file:
                text = open_file.read()
                self.codeEdit.setPlainText(text)

    def open_folder(self):
        if not (self.sender() is None):
            if self.sender().text() == "Folder":
                dir = QFileDialog.getExistingDirectory(self,
                                                       "Select Project",
                                                       self.dir_path,
                                                       options=QFileDialog.DontUseNativeDialog
                                                       )
                if dir != "":
                    self.dir_path = dir

        # Files Tree
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(self.dir_path)

        self.treeView.setModel(self.model)
        self.treeView.setAnimated(True)
        self.treeView.setIndentation(20)
        self.treeView.setSortingEnabled(True)
        self.treeView.setRootIndex(self.model.index(self.dir_path))
        self.treeView.doubleClicked.connect(self.selectFile)

    def closeFile(self):
        self.file_path = ""
        self.file_type = ""
        self.dir_path = ""
        self.codeEdit.clear()

        self.open_folder()
        self.write_settings()

    def updateWindow(self):
        # Save Changes
        self.save_file()

        # Update Encoding
        self.encoding = self.encodingList.currentText()

        # Load Updating Settings
        self.load_settings(["theme", "font_family", "python_path"])

        # Set Current File
        if len(self.file_path) > 0 and os.path.exists(self.file_path):
            self.currentFile.setText(f" {self.file_path}")
        else:
            self.currentFile.setText("")

        # Try Set Python Version
        try:
            self.pythonVersion.setText(os.popen(f"{self.python_path} -V", ).read().strip())

        except Exception:
            self.pythonVersion.setText("No Interpreter")

        # Set Standard Type
        self.file_type = os.path.splitext(self.file_path)[-1]

        # Set Font
        self.codeEdit.setStyleSheet(f"font-family: {self.font_family};")
        self.console.setStyleSheet(f"font-family: {self.font_family};")

        # Set Widget Color Scheme
        widget_colors = \
            self.cur_color.execute("""SELECT colors FROM widget_themes WHERE name=?""", (self.theme,)).fetchall()[
                0][0]
        self.setStyleSheet(widget_colors)

        # Data Transfer To Settings
        self.settApp.colors = widget_colors
        self.settApp.encoding = self.encoding

        # Set Code Color Scheme
        try:
            colors = json.loads(
                self.cur_color.execute(
                    """SELECT colors FROM code_themes WHERE file_type=? AND name=?""",
                    (self.file_type, self.theme)).fetchall()[0][0])

            self.highlight = Highlighter(self.codeEdit.document(), colors=colors)


        except Exception:
            colors = json.loads(
                self.cur_color.execute(
                    """SELECT colors FROM code_themes WHERE file_type="*" AND name=?""",
                    (self.theme,)).fetchall()[0][0])

            self.highlight = Highlighter(self.codeEdit.document(), colors=colors)

    def runCode(self):
        if not os.path.exists(self.file_path):
            output = b""
            error = b"Invalid File Name"

        else:
            command = f"{self.python_path} {os.path.abspath(self.file_path)}"
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            shell=True)

            output, error = self.process.communicate()
            if error is None:
                error = ""

        console_text = f"===== {self.file_path} =====<br><br>"
        console_text += "{}<br>".format(output.decode('utf-8').replace('\n', '<br>'))
        console_text += f'<span style="color: #e34034;">{error.decode("utf-8")}</span>'

        self.console.setHtml(console_text)

    def stopCode(self):
        pass

    def createControlPoint(self):
        try:
            if self.file_path != "" and self.codeEdit.toPlainText().strip() != "":
                code = self.cur_control_point.execute(
                    """SELECT code FROM points WHERE file_path=?""",
                    (self.file_path,)).fetchall()

                # Check Record
                if len(code) == 0:
                    self.cur_control_point.execute(
                        """INSERT INTO points(file_type, file_path, code) VALUES(?, ?, ?)""",
                        (self.file_type, self.file_path, self.codeEdit.toPlainText()))
                    self.con_control_point.commit()

                else:
                    self.cur_control_point.execute(
                        """UPDATE points SET code=? WHERE file_type=? AND file_path=?""",
                        (self.codeEdit.toPlainText(), self.file_type, self.file_path))
                    self.con_control_point.commit()

        except Exception:
            pass

    def loadControlPoint(self):
        try:
            code = self.cur_control_point.execute(
                """SELECT code FROM points WHERE file_type=? AND file_path=?""",
                (self.file_type, self.file_path)).fetchall()

            # Check Record
            if len(code) != 0:
                self.codeEdit.setPlainText(code[0][0])
            else:
                console_text = f"===== {self.file_path}=====<br><br>"
                console_text += "<span style='color: #e34034;'>Control Point Not Found</span>"

                self.console.setHtml(console_text)

        except Exception:
            pass

    def load_settings(self, toRecord):
        with open(pathAppData + "settings.json", encoding="utf-8") as sett_file:
            settings = json.loads(sett_file.read())
            for item in toRecord:
                exec(f"self.{item} = settings['{item}']")

        # Loads All Encodings
        self.encodingList.clear()
        self.encodingList.addItems(allEncodings)
        self.encodingList.setCurrentIndex(self.encodingList.findText(self.encoding))

    def write_settings(self):
        with open(pathAppData + "settings.json", mode="w", encoding="utf-8") as sett_file:
            data = {"file_path": self.file_path,
                    "file_type": self.file_type,
                    "dir_path": self.dir_path,
                    "theme": self.theme,
                    "font_family": self.font_family,
                    "python_path": self.python_path,
                    "encoding": self.encoding
                    }

            json.dump(data, sett_file, indent=4)

    def set_icons(self):
        # Window
        self.setWindowIcon(QIcon(pathIcons + "logo.png"))

        # Buttons
        self.startButton.setIcon(QIcon(pathIcons + "run.png"))
        self.startButton.setIconSize(QIcon(pathIcons + "run.png").availableSizes()[0])
        self.stopButton.setIcon(QIcon(pathIcons + "stop.png"))

        # Menu
        self.menuOpen.setIcon(QIcon(pathIcons + "open.png"))
        self.actionRun.setIcon(QIcon(pathIcons + "run.png"))
        self.actionSettings.setIcon(QIcon(pathIcons + "settings.png"))

    def set_commands(self):
        # Menu button
        self.actionPython_File.triggered.connect(self.create_file)
        self.actionOther_File.triggered.connect(self.create_file)

        self.actionSave_as.triggered.connect(self.save_file)

        self.actionPython_File_2.triggered.connect(self.open_file)
        self.actionFile_2.triggered.connect(self.open_file)
        self.actionFolder.triggered.connect(self.open_folder)
        self.actionSettings.triggered.connect(lambda func: self.settApp.show())
        self.actionClose.triggered.connect(self.closeFile)
        self.actionExit_2.triggered.connect(self.close)

        self.actionRun.triggered.connect(self.runCode)

        self.actionCreate_Control_Point.triggered.connect(self.createControlPoint)
        self.actionLoad_Control_Point.triggered.connect(self.loadControlPoint)

        # Other Button
        self.startButton.clicked.connect(self.runCode)
        self.startButton.setShortcut("shift+f10")
        self.stopButton.clicked.connect(self.stopCode)

    def closeEvent(self, a0):
        self.save_file()
        self.write_settings()

        self.settApp.close()

        self.con_color.close()
        self.con_control_point.close()
