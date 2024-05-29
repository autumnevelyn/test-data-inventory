import csv
import numpy as np
from PIL import Image
import os

files_base_path = 'C:\\Users\\s0141759\\repos\\MobileBioSDK_QA'
output_dir = 'C:\\Users\\s0141759\\Desktop\\test_data_inventory\\generated'

def convert_to_png(relative_path, file_name, dimensions, color_mode):
    # Parse dimensions
    width, height = map(int, dimensions.split('x'))
    # Determine pixel depth
    if color_mode == 'BW':
        pixel_depth = 1
        mode = 'L'  # 8-bit pixels, black and white
    elif color_mode == 'RGB':
        pixel_depth = 3
        mode = 'RGB'
    elif color_mode == 'BGR':
        pixel_depth = 3
        mode = 'RGB'
    elif color_mode == 'RGBA':
        pixel_depth = 4
        mode = 'RGBA'
    else:
        return
    
    # Read binary data from the file
    file_path = os.path.join(files_base_path, relative_path[1:],file_name)
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    # Create numpy array from raw data
    image_array = np.frombuffer(raw_data, dtype=np.uint8)
    
    if len(image_array) != width * height * pixel_depth:
        print(f"Error: File size does not match dimensions for {file_path}")
        return
    
    # Image.fromarray() function is expecting a 2-dimensional array for 'L' mode images 
    if pixel_depth == 1:
        image_array = image_array.reshape((height, width))
    else:
        image_array = image_array.reshape((height, width, pixel_depth))
    
    # Handle BGR color mode by swapping red and blue channels
    if color_mode == 'BGR':
        image_array = image_array[..., [2, 1, 0]]  # Swap the first and last channel

    # Create a Pillow Image
    image = Image.fromarray(image_array, mode=mode)
    
    # Save the image as PNG
    output_path = os.path.join(output_dir, relative_path[1:])
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image.save(os.path.join(output_path ,file_name + '.png'))
    print(f"Converted {file_path}")

def process_csv(csv_path):
    # Open and read the CSV file
    with open(csv_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  # Skip header row

        previous = ''
        for row in csvreader:
            # Extract relevant columns by index
            relative_path = row[0]
            file_name = row[1]
            extension = row[2]
            dimensions = row[6]
            color = row[7]
            
            # Apply the filters
            if (extension in ['.data', '.raw'] and
                dimensions not in ['N/F', 'N/A'] and
                color in ['BW', 'RGB', 'BGR', 'RGBA'] and
                file_name!=previous):
                convert_to_png(relative_path, file_name, dimensions, color)
                previous = file_name

# Path to the CSV file
csv_path = 'C:\\Users\\s0141759\\Desktop\\test_data_inventory\\data-QA.csv'
process_csv(csv_path)
print(f"Successfully converted all images. Output saved to {output_dir}")
