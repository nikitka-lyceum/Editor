import sys
import ctypes
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from classes.Editor import EditorCode
from config import pathAppData

myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(pathAppData + "icon/logo.png"))
    codeEditor = EditorCode()
    codeEditor.show()
    sys.exit(app.exec())
