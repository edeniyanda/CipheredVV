import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QObject, pyqtSignal

class ChildWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Child Window")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        maximize_button = QPushButton("Maximize")
        maximize_button.clicked.connect(self.maximize_window)

        minimize_button = QPushButton("Minimize")
        minimize_button.clicked.connect(self.minimize_window)

        layout.addWidget(maximize_button)
        layout.addWidget(minimize_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Store the initial window geometry
        self.initial_geometry = self.geometry()

    def maximize_window(self):
        self.setGeometry(self.initial_geometry)
        self.showNormal()

    def minimize_window(self):
        self.showMinimized()

    def restore_child_window(self):
        if self.isMinimized():
            self.showNormal()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        self.child_window = ChildWindow(self)

        layout = QVBoxLayout()

        open_child_button = QPushButton("Open Child Window")
        open_child_button.clicked.connect(self.open_child_window)

        layout.addWidget(open_child_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_child_window(self):
        self.child_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
