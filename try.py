import os

file_path = 'C:/Users/HP/Desktop/testC:/Users/HP/Documents/help multism.txt'

# Split the file path into the directory path and the file name with extension
directory, filename = os.path.split(file_path)

# Split the file name and extension
name, extension = os.path.splitext(filename)

# Join the directory path and file name without extension
new_file_path = os.path.join(directory, name)

print(new_file_path)
