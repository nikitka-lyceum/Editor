import sys
import ctypes
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from classes.Editor import EditorCode
from config import pathIcons

myappid = 'mycompany.myproduct.subproduct.version' #qwerty
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(pathIcons + "logo.png"))
    codeEditor = EditorCode()
    codeEditor.show()
    sys.exit(app.exec())
