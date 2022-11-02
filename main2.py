import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from classes.Editor import EditorCode

if __name__ == "__main__":
    app = QApplication(sys.argv)
    codeEditor = EditorCode()
    codeEditor.show()
    sys.exit(app.exec())
