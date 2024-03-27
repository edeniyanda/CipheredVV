import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QLabel, QPushButton, QSpinBox, QTableWidget, QDialog, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUiType

def get_resource_path(relative_path):
    """
    Get the absolute path to the resource based on whether the script is running as an executable or as a script.
    """
    if getattr(sys, 'frozen', False):
        # Running as an executable, use sys._MEIPASS to access bundled files
        base_path = sys._MEIPASS
    else:
        # Running as a script, use the script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    resource_path = os.path.join(base_path, relative_path)
    return resource_path

EncrypPromptui, _ = loadUiType(get_resource_path('../ui/EncryptionUi.ui'))

# Main application window
class EncryptWindow(QMainWindow, EncrypPromptui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setStyleSheet("QMainWindow {border-radius: 10px;}")
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.pushButtonCancel.clicked.connect(self.close)
        self.pushButtonBrowse.clicked.connect(self.openFileDialogue)
        self.pushButtonProceed.clicked.connect(self.proceed)
        self.pushButtonCancel2.clicked.connect(self.close)

    def openFileDialogue(self):
        home_dir = os.path.expanduser("~")

        # Set the default directoxry to the desktop directory
        self.defaultDir = os.path.join(home_dir, "Desktop")
        file_types = "Text files (*.txt *.docx *.pdf *.rtf *.odt);;" \
                    "Audio files (*.mp3);;" \
                    "Video files (*.mp4);;" \
                    "Image files (*.jpg *.png *.gif);;" \
                    "Database files (*.sqlite *.db *.mdb);;" \
                    "Spreadsheet files (*.xlsx);;" \
                    "CSV files (*.csv)"
        try:
            self.file, _ = QFileDialog.getOpenFileName(self,
                                                    "Select a file to encrypt",
                                                    self.defaultDir,
            
                                                   file_types)
            self.lineEditPath.setText(self.file)
        except FileNotFoundError:
            pass
    def proceed(self):
        self.filePath = self.lineEditPath.text()
        if self.filePath:
            if os.path.exists(self.filePath):
                ...
            else:
                QMessageBox.critical(self,
                                     "Error",
                                     f"'{self.filePath}' is not a valid Path",
                                     )

    
    def displayWindow(self):
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = EncryptWindow()
    mainWindow.displayWindow()
    sys.exit(app.exec_())
