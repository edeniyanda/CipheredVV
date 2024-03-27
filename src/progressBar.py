import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QLabel, QPushButton, QSpinBox, QTableWidget, QDialog, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUiType
from appmodules import encryptFile, tellIcon
# from encryptwindow import EncryptWindow


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

progressBarui, _ = loadUiType(get_resource_path('../ui/progeressBar.ui'))
counter = 0
# Main application window
class progressBarWindow(QMainWindow, progressBarui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.infoShow = {
            30 : "...getting ciphers",
            60 : "...building chiphers",
            80 : "...getting ready",
            100 : "Completed"
        }



    def progress(self):
        global counter
        
        self.progressBar.setValue(counter)
        
        if counter > 100:
            self.timer.stop()
            self.close()
        messageToShow = self.infoShow.get(counter)
        if messageToShow:
            self.labelMessage.setText(messageToShow)

        counter += 1
        ...
    def displayWindow(self):
        # ProgresBar timer 
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        
        self.timer.start(35)
        self.show()




