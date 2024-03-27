import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class ChildWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Child Window")
        self.setGeometry(100, 100, 200, 100)

class ParentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parent Window")
        self.setGeometry(300, 300, 300, 200)
        self.button = QPushButton("Open Child Window", self)
        self.button.setGeometry(100, 100, 150, 50)
        self.button.clicked.connect(self.openChildWindow)
        self.childWindow = None

    def openChildWindow(self):
        if not self.childWindow:
            self.childWindow = ChildWindow(self)
            self.childWindow.show()

    def closeEvent(self, event):
        if self.childWindow and self.childWindow.isVisible():
            event.ignore()  # Ignore the close event
        else:
            event.accept()  # Accept the close event

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ParentWindow()
    mainWindow.show()
    sys.exit(app.exec_())
