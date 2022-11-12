from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class Example(QMainWindow):
	def __init__(self):
		super().__init__()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	ex = Example()
	ex.show()

	sys.exit(app.exec())