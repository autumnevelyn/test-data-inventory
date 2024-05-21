import csv

def read_csv(file_path):
    """
    Read CSV file and return a list of its rows.
    """
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows

def compare_and_write(first_file, second_file, output_file):
    """
    Compare file names in the first file with the name column in the second file,
    and write rows from the first file whose names were not found in the second file.
    """
    # Read CSV files
    first_data = read_csv(first_file)
    second_data = read_csv(second_file)
    
    # Extract file names from both files
    first_names = set(row[1] for row in first_data)
    second_names = set(row[2] for row in second_data)
    
    # Find names in the first file that are not in the second file
    unique_names = first_names - second_names
    
    # Write rows with unique names to the output file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in first_data:
            if row[1] in unique_names:
                writer.writerow(row)

# File paths
new_file_path = "C:\\Users\\s0141759\\Desktop\\test_data_inventory\\test_file_info.csv"  # Replace with the path to the first CSV file
original_file_path = "C:\\Users\\s0141759\\Desktop\\test_data_inventory\\Data_inventory.csv"  # Replace with the path to the second CSV file
output_file_path = "unique_test_files_info.csv"  # Replace with the desired path for the output file

# Compare and write unique rows
compare_and_write(new_file_path, original_file_path, output_file_path)

print("Unique names written to", output_file_path)
