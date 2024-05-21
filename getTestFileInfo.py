import os
import csv

# Traverses the entire file tree in the provided from the provided path and lists all the files found
# For each file we save it's filename, path relative to the root of the search and it's data type

def list_files(startpath):
    # Create a list to store file information
    file_list = []
    
    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(startpath):
        for file in files:
            # Extract file name, relative path, and extension
            file_name = file
            relative_path = os.path.relpath(root, startpath)
            file_extension = os.path.splitext(file)[1]
            
            # Append file information to the list
            file_list.append((relative_path, file_name, file_extension if file_extension else "-"))
            print(f"'{file}' found")
    
    return file_list

# Specify the folder to start traversal
start_folder = input("Enter the folder path to start traversal: ")

# Get the list of files
files_info = list_files(start_folder)

# Specify the CSV file path to save the data
csv_file = "test_files_info.csv"

# Write the file information to a CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Relative Path', 'File Name', 'File Extension'])
    writer.writerows(files_info)

print(f"\nFound {len(files_info)} files.")
print(f"Output saved successfully to '{csv_file}'.")
