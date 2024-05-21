import csv

def read_csv(file_path):
    """
    Read CSV file and return a list of its rows.
    """
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows

def extract_descriptions(first_file, second_file, output_file):
    # Read CSV files
    first_data = read_csv(first_file)
    second_data = read_csv(second_file)
    
    # Extract file names from both files
    first_names = list(row[1] for row in first_data)
    second_names = list(row[2] for row in second_data)
    
    # Write rows with unique names to the output file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in first_data:
            if row[1] in second_names:
                index = second_names.index(row[1])
                org_row = second_data[index]
                writer.writerow(row + [org_row[7]])

# File paths
new_file_path = "C:\\Users\\s0141759\\Desktop\\test_data_inventory\\test_files_info.csv"  # Replace with the path to the first CSV file
original_file_path = "C:\\Users\\s0141759\\Desktop\\test_data_inventory\\Data_inventory.csv"  # Replace with the path to the second CSV file
output_file_path = "files_with_descriptions.csv"  # Replace with the desired path for the output file

# Compare and write unique rows
extract_descriptions(new_file_path, original_file_path, output_file_path)

print("Unique names written to", output_file_path)
