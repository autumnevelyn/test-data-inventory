import time
import os
import csv
import re

# Specify the Java project folder, unique names CSV, and output CSV
java_project_folder = "C:\\Users\\s0141759\\repos\\MobileBioSDK_QA\\Java\\src\\test\\java"
file_info_csv = 'test_files_info.csv'  # Output CSV from the previous script
output_csv = 'output_data.csv'  # Output CSV for storing extended rows


def find_junit_test_names(filename, content):
    # Look for all methods declarations containing the file name we are looking for. Capturing the method name
    # this is done by looking for '@' symbol marking an annotation infront of the method followed by 'public' optionally 'static' and 'void' 
    # then function name followed by parenthesis. Then we do a lookahead to see if there is an occurence of the filename we are looking for
    # before we encounter another '@' starting the cycle from start again

    if(len(filename) == 0): raise ValueError("Filename cannot be empty")

    # Escape the filename
    filename_esc = re.escape( os.path.splitext(filename)[0] if os.path.splitext(filename)[1] == '.data' else filename)

    # expression to match the name of the test file in parenthesis
    filename_regex = rf'"(?:[^@"]*?[\\\/])?{filename_esc}(?:\.data)?"'

    res = []
    if (re.search(filename_regex, content)):
        # Finds annotated methods that contain the searched filename, capture the name of the method as well as any potential dimentions of the image       
        matches = re.findall(rf'@[^@]*?public\s?(?:static)?\s+?void\s+?(\w+)\s*?\(\)(?=(?:[^@]*?{filename_regex}(?:[^\d;]*?,\s*(\d*),\s*(\d*))?))', content, re.DOTALL)
        
        # This lets us see if a file contains the metched filename but it is not contained in an annotated method
        # this requires an exception for very short filenames, to avoid extra false matches
        res = matches if matches or len(filename_esc) == 1 else [('','','')]

    return res

def search_and_extend(java_project_folder, file_info_csv, output_csv):
    # Read file names from CSV
    rows = []
    with open(file_info_csv, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Store headers
        for row in reader:
            rows.append(row)

    # Create a list to store extended rows
    extended_rows = []

    # Write extended rows to the output CSV file
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers + ['Package','Test','Dimensions'])  # Write headers

        # Iterate through Java project folder and its subfolders
        for original_row in rows:
            test_file_name = original_row[1]
            found_flag = False
            for root, dirs, files in os.walk(java_project_folder):
                for project_file in files:
                    # Check if the file is a Java file
                    if project_file.endswith('.java'):
                        file_path = os.path.join(root, project_file)
                        package = os.path.relpath(root, java_project_folder).replace(os.path.sep, '.')
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as java_file:
                            content = java_file.read()
                            # Search for each file name in the Java file
                            matches = find_junit_test_names(test_file_name, content)
                            if matches:
                                found_flag = True
                                for test_name, width, height in matches:
                                    test_field = f'{os.path.splitext(project_file)[0]}.{test_name}' if test_name else os.path.splitext(project_file)[0]
                                    dimensions_field = f'{width}x{height}' if (width and height) else 'NF'
                                    extended_row = original_row + [package, test_field, dimensions_field]
                                    
                                    writer.writerow(extended_row)
                                    print(extended_row)
            # If the string was not found anywhere, add "NF" to the new columns
            if not found_flag:
                extended_row = original_row + ['NF', 'NF', 'NF']
                
                writer.writerow(extended_row)
                print(extended_row)

# Perform the search and extend rows
start = time.time()
search_and_extend(java_project_folder, file_info_csv, output_csv)

print(f"\n{round(time.time()-start,2)}s")
print(f"Search completed and data saved to '{output_csv}'")