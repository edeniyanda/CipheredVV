import os
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QFileDialog, QMessageBox
# from mainwindow import MainWindow



# Determine the user's home directory
home_dir = os.path.expanduser("~")
# Set the default directory to the desktop directory
defaultDir = os.path.join(home_dir, "Desktop")


class encryptFile:
    def __init__(self, file_path:str) -> None:
        self.file_path = file_path
        
    def generate_key(self):
        return Fernet.generate_key()

    def encrypt_file(self, key):
        cipher = Fernet(key)
        with open(self.file_path, "rb") as file:
            data = file.read()
            encrypted_data = cipher.encrypt(data)

        return encrypted_data



        

    



            
            

            

class decryptFile:
    def __init__(self, file_path:str, path_to_save_decrypted:str) -> None:
        self.file_path = file_path
        self.path_to_save_decrypted = path_to_save_decrypted  
        
    def load_key(self, path_to_secret_key):
        return open(path_to_secret_key, "rb").read()

    def decrypt_file(self, key):
        cipher = Fernet(key)
        with open(self.file_path, "rb") as file:
            encrypted_data = file.read()
            decrypted_data = cipher.decrypt(encrypted_data)
        
        
        # This section tries to get the name of the file from the path provided by the user
        file_path_in_list = list(self.file_path)
        ind = file_path_in_list[::-1].index("\\")
        file_path_in_str = "".join(file_path_in_list[::-1][:ind][::-1])
        
        if ".enc" in file_path_in_str:
            file_name = file_path_in_str[:-4]
        else:
            file_name = file_path_in_str
            
        path_to_save_to = self.path_to_save_decrypted + "\\" + file_name
        with open(path_to_save_to, "wb") as file:
            file.write(decrypted_data)
    
    

            
