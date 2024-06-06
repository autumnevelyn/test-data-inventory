import os

# Function to change file extensions based on filename pattern
def change_file_extensions(base_directory):
    # Walk through all directories and files
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            # Full path of the file
            file_path = os.path.join(root, file)
            # Check if the file ends with .999 and has .bin extension
            if file.endswith('.999.bin'):
                new_file_path = file_path.replace('.999.bin', '.jpg')
                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_path} -> {new_file_path}")
            # Check if the file ends with .009 and has .bin extension
            elif file.endswith('.009.bin'):
                new_file_path = file_path.replace('.009.bin', '.wsq')
                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_path} -> {new_file_path}")

# Example usage
base_directory = './extracted'  # Change this to your base directory path

change_file_extensions(base_directory)
