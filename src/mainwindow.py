import os
import sys
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QLabel, QPushButton, QSpinBox, QTableWidget, QDialog, QFileDialog
# from PyQt5.QtGui import QFont, QPixmap
from PyQt5.uic import loadUiType
import qdarkstyle
from functools import partial
from appmodules import encryptFile


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

# Constants and configuration
APP_NAME = "CipheredVV"
ui, _ = loadUiType(get_resource_path('../ui/mainwindow.ui'))

# Main application window
class MainWindow(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.handlePushButtons()
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        # self.setStyleSheet(dark_stylesheet)   
        self.setFixedSize(1052,581)
        self.tabWidget.tabBar().setVisible(False) # Disable Tab Visibility
        self.tabWidget.setCurrentIndex(0) # Set the current index of the tab WIdget to the first tab

    def handlePushButtons(self):
        self.pushButtonEncrypt.clicked.connect(partial(self.changeTabWidgetIndex, 1))
        self.pushButtonDecrypt.clicked.connect(partial(self.changeTabWidgetIndex, 2))
        self.pushButtonHomeE.clicked.connect(partial(self.changeTabWidgetIndex, 0))
        self.pushButtonHomeD.clicked.connect(partial(self.changeTabWidgetIndex, 0))
        self.toolButtonBrowse.clicked.connect(self.openFile)
        

    # Change Main Widget 
    def changeTabWidgetIndex(self, index_position:int):
        self.tabWidget.setCurrentIndex(index_position)
        
    def openFile(self):
        file_types = "Text files (*.txt *.docx *.pdf *.rtf *.odt);;" \
                    "Audio files (*.mp3);;" \
                    "Video files (*.mp4);;" \
                    "Image files (*.jpg *.png *.gif);;" \
                    "Database files (*.sqlite *.db *.mdb);;" \
                    "Spreadsheet files (*.xlsx);;" \
                    "CSV files (*.csv)"

        file, _ = QFileDialog.getOpenFileName(self,
                                                "Select a file to encrypt",
                                                "/home",
                                                file_types)
    
    

# Application entry point
def main():
    # Initialize the application
    app = QApplication(sys.argv)
    # Create and show the main window
    mainWindow = MainWindow()
    mainWindow.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

# Entry point for standalone execution
if __name__ == "__main__":
    main()
