import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QLabel, QPushButton, QSpinBox, QTableWidget, QDialog, QFileDialog, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUiType
import qdarkstyle
from functools import partial
from appmodules import encryptFile, tellIcon
from encryptwindow import EncryptWindow
from progressBar import progressBarui



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
        self.setStyleSheet(dark_stylesheet)
        self.setFixedSize(850,554)
        self.tabWidget.tabBar().setVisible(False) # Disable Tab Visibility
        self.tabWidget.setCurrentIndex(0) # Set the current index of the tab WIdget to the first tab
        # self.progressBar = progressBarui()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        self.pushButtonEncrypt.setGraphicsEffect(shadow)

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
        self.encryptab = EncryptWindow()
        self.encryptab.displayWindow()


        with open(get_resource_path("filepath.txt"), "r") as fhand:
            self.file = fhand.read()

            ...
        #     if self.file:
        #         dir, filname = os.path.split(self.file)
        #         filename, extension = os.path.splitext(filname)
        #         iconToShow = tellIcon(extension)  
        #         icon_filename = iconToShow.tell() 
        #         pixmap_path = get_resource_path(f"../assets/img/icon/{icon_filename}")
        #         if os.path.exists(pixmap_path):
        #             pixmap = QPixmap(pixmap_path)
        #             self.iconLabel.setPixmap(pixmap)
        #         self.lineEditfilename.setReadOnly(False)
        #         self.lineEditfilename.setText(filname)
        #         self.lineEditfilename.setReadOnly(True)
        #         self.encryptFile(self.file)
        # except FileNotFoundError:
        #     pass
    
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
    def closeEvent(self, event):
        if self.encryptab and self.encryptab.isVisible():
            event.ignore()
            QMessageBox.critical(self,
                                 "Error",
                                 "Closed the Browse Window first")
            self.encryptab.initial_geometry = self.encryptab.geometry()
            self.encryptab.setGeometry(self.encryptab.initial_geometry)
            # self.encryptab.showNormal()
            self.encryptab.setVisible(True)  # Ignore the close event
        else:
            reply = QMessageBox.question(
                                    self,
                                    'Confirm Exit',
                                    'Are you sure you want to exit?',
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No
                                )
            if reply == QMessageBox.Yes:
                event.accept()  # Close the application
            else:
                event.ignore()  # Ignore the close event




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
