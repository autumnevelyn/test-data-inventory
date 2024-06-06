import os
import base64
import xml.etree.ElementTree as ET
import csv

# Define the directory containing the XML files
xml_directory = 'C:\\Users\\s0141759\\repos\\MobileBioSDK_QA\\assets\\nist-tests-extension-data\\AN2011_SampleData\\NIEM XML Encoding'
output_directory = 'generated\\nist_contents'

# Table 201 for image compression extensions
compression_extensions = {
    "NONE": ".data",
    "WSQ20": ".wsq",
    "JPEGB": ".jpg",
    "JPEGL": ".jpg",
    "JP2": ".jp2",
    "JP2L": ".jp2",
    "PNG": ".png"
}


# CSV output file
csv_file = os.path.join(output_directory, 'image_data.csv')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Prepare CSV file for writing
with open(csv_file, mode='w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['FileName', 'Width', 'Height', 'BitsPerPixel'])

    # Process each XML file in the directory
    for xml_filename in os.listdir(xml_directory):
        if xml_filename.endswith('.xml'):
            xml_path = os.path.join(xml_directory, xml_filename)
            try:
                tree = ET.parse(xml_path)
            except:
                print(f'Could not parse {xml_filename}')
                continue
            root = tree.getroot()
            
            index = 1

            # Find all tags ending in 'ImageRecord'
            for child in root:
                if 'ImageRecord' not in child.tag: continue

                for image_tag in child.findall("./*[nc:BinaryBase64Object]", namespaces={'nc': 'http://niem.gov/niem/niem-core/2.0'}):
                    try:
                        record_name = image_tag.tag.split('}')[-1]  # Get the tag name without namespace
                        # Extract relevant data
                        base64_data = image_tag.find('.//nc:BinaryBase64Object', namespaces={'nc': 'http://niem.gov/niem/niem-core/2.0'}).text
                        compression_text = image_tag.find('.//biom:ImageCompressionAlgorithmText', namespaces={'biom': 'http://niem.gov/niem/biometrics/1.0'})
                        compression_text = None if compression_text is None else compression_text.text
                        compression_code = image_tag.find('.//biom:ImageCompressionAlgorithmCode', namespaces={'biom': 'http://niem.gov/niem/biometrics/1.0'})
                        compression_code = None if compression_code is None else int(compression_code.text)
                        bpp = image_tag.find('.//biom:ImageBitsPerPixelQuantity', namespaces={'biom': 'http://niem.gov/niem/biometrics/1.0'}).text if(compression_text == 'NONE' or compression_code==0) else None
                        width = image_tag.find('.//biom:ImageHorizontalLineLengthPixelQuantity', namespaces={'biom': 'http://niem.gov/niem/biometrics/1.0'}).text
                        height = image_tag.find('.//biom:ImageVerticalLineLengthPixelQuantity', namespaces={'biom': 'http://niem.gov/niem/biometrics/1.0'}).text

                        # Decode base64 data
                        binary_data = base64.b64decode(base64_data)

                        # Determine file extension
                        extension = compression_extensions[compression_text] if compression_text else list(compression_extensions.values())[compression_code]

                        # Create output file name
                        output_filename = f"{os.path.splitext(xml_filename)[0]}_{record_name}_{index}{extension}"
                        output_path = os.path.join(output_directory, output_filename)

                        # Write binary data to file
                        with open(output_path, 'wb') as output_file:
                            output_file.write(binary_data)

                        # Write metadata to CSV
                        csvwriter.writerow([output_filename, width, height, bpp if bpp else ''])
                        print(output_filename)
                    except:
                        print(f"Could not read {record_name} record in {xml_filename}. Skipping")

                # Increment index for next image of the same type
                index += 1
