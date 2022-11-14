import sys
import ctypes
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from classes.Editor import EditorCode
from config import pathIcons

editorApp = 'nikEditor.Editor.Python.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(editorApp)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(pathIcons + "logo.png"))
    codeEditor = EditorCode()
    codeEditor.show()
    sys.exit(app.exec())
