import os
from PIL import Image
import csv

# Specify the directory containing the JPG files
image_dir = 'C:\\Users\\s0141759\\repos\\MobileBioSDK_QA\\assets\\frp'
output_csv = 'image_dimensions.csv'

# List to store image details
image_details = []

# Loop through all files in the directory
for filename in os.listdir(image_dir):
    if filename.lower().endswith('.jpg'):
        # Open the image file
        with Image.open(os.path.join(image_dir, filename)) as img:
            width, height = img.size
            dimensions = f"{width}x{height}"
            image_details.append([filename, dimensions])

# Write the details to a CSV file
with open(output_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['name', 'dimensions'])
    csvwriter.writerows(image_details)

print(f"Image dimensions have been written to {output_csv}")
