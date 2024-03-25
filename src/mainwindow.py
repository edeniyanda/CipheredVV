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
        self.setFixedSize(850,554)
        self.tabWidget.tabBar().setVisible(False) # Disable Tab Visibility
        self.tabWidget.setCurrentIndex(0) # Set the current index of the tab WIdget to the first tab

    def handlePushButtons(self):
        self.pushButtonEncrypt.clicked.connect(partial(self.changeTabWidgetIndex, 1))
        self.pushButtonDecrypt.clicked.connect(partial(self.changeTabWidgetIndex, 2))
        self.pushButtonHomeE.clicked.connect(partial(self.changeTabWidgetIndex, 0))
        self.pushButtonHomeD.clicked.connect(partial(self.changeTabWidgetIndex, 0))
        self.uploadButton.clicked.connect(self.openFile)
        

    # Change Main Widget 
    def changeTabWidgetIndex(self, index_position:int):
        self.tabWidget.setCurrentIndex(index_position)
        
    def openFile(self):
        # Determine the user's home directory
        home_dir = os.path.expanduser("~")

        # Set the default directory to the desktop directory
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
            
            if self.file:
                dir, filname = os.path.split(self.file)
                filname, extention = os.path.splitext(filname)   
                self.lineEditfilename.setText(filname)
                self.encryptFile(self.file)
        except FileNotFoundError:
            pass
    
    def encryptFile(self, filename):
        goEncrypt = encryptFile(filename)
        self.secretKey= goEncrypt.generate_key()
        self.encryptedData = goEncrypt.encrypt_file(self.secretKey)
        QMessageBox.information(self,
                                "Encryption Status",
                                "File Encrypted sucessfully"
                                )
        self.saveEncrypted(self.encryptedData)
        self.save_key(self.secretKey)

        ...


    def saveEncrypted(self, dataToSave):

        save_folder_path = QFileDialog.getExistingDirectory(self,
                                                            "Select Folder to Save Encrypted File",
                                                            self.defaultDir
                                                           )
        if len(save_folder_path) == 0:
            save_folder_path = "/Desktop"
        if save_folder_path:
            dir, selectedfilename = os.path.split(self.file)

            self.save_encrypted_path = save_folder_path + "/" + selectedfilename
        
            try:
                with open(self.save_encrypted_path + ".enc", "wb") as file:
                    file.write(dataToSave)
                QMessageBox.information(self,
                                        "Encryption Status",
                                        "Encrypted file saved sucessfully"
                                        )
            except Exception as e:
                QMessageBox.information(self,
                                        "Encryption Status",
                                        f"Error Message: {e}"
                                        )
                
        else:
            QMessageBox.information(self,
                                        "Encryption Status",
                                        "Invalid Path"
                                        )
            self.saveEncrypted(self.encryptedData)

            
    def save_key(self, key, filename="secret.key"):
        saveKey_folder_path = QFileDialog.getExistingDirectory(self,
                                                    "Select Folder to Save Encrytion Secret Key",
                                                    self.defaultDir
        )
        if saveKey_folder_path:
            path_to_save = saveKey_folder_path + "/" + filename
            with open(path_to_save, "wb") as key_file:
                key_file.write(key)

            QMessageBox.information(self,
                                    "Encryption Status",
                                    "Secret Key has been save sucessfully"
                                    )
        else:
            QMessageBox.information(self,
                                        "Encryption Status",
                                        "Invalid Path, Pleaee select a folder"
                                        )
            self.save_key(self.secretKey)



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
