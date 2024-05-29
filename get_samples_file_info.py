import os
import csv

path_to_repos = 'C:\\Users\\s0141759\\repos'
sdk_samples_dir = f'{path_to_repos}\\BioSDK_Default'
sample_assets_dirs = [f'{path_to_repos}\\MobileBioSDK_QA\\samples\\resources\\FaceSample',
f'{sdk_samples_dir}\\tools\\sample_tests\\resources\\FaceSample',
f'{sdk_samples_dir}\\release\\biosdk-android\\sample\\FingerSample\\app\\src\\main\\assets',
f'{sdk_samples_dir}\\release\\biosdk-android\\sample\\IrisSample\\app\\src\\main\\assets',
f'{sdk_samples_dir}\\release\\biosdk-android\\sample\\NistSample\\app\\src\\main\\assets',
f'{sdk_samples_dir}\\release\\biosdk-java\\sample\\FaceLiteSample\\src\\main\\resources',
f'{sdk_samples_dir}\\release\\biosdk-java\\sample\\FacePadSample\\src\\main\\resources',
f'{sdk_samples_dir}\\release\\biosdk-java\\sample\\FingerSample\\src\\main\\resources',
f'{sdk_samples_dir}\\release\\biosdk-java\\sample\\FrpFaceMatchingSample\\src\\main\\resources',
f'{sdk_samples_dir}\\release\\biosdk-java\\sample\\ImageSample\\src\\main\\resources',
f'{sdk_samples_dir}\\release\\biosdk-java\\sample\\IrisSample\\src\\main\\resources',
f'{sdk_samples_dir}\\release\\biosdk-java\\sample\\NistSample\\src\\main\\resources',
f'{sdk_samples_dir}\\release\\biosdk-linux\\sample\\c++\\Frp\\resources',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\c++\\FaceLiteSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\c++\\FingerSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\c++\\Frp\\resources',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\c++\\ImageSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\c++\\IrisSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\c++\\NistSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\c++\\NistSample\\resources',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\FaceLiteSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\FingerSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\Frp\\DetectImage\\Photos',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\Frp\\FaceCaptureSample\\Photos',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\Frp\\FaceMatch\\Photos',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\Frp\\FaceSearch\\Photos',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\Frp\\PassiveCaptureSample\\PassivePhotos',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\ImageSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\IrisSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\NistSample',
f'{sdk_samples_dir}\\release\\biosdk-windows\\sample\\csharp\\NistSample\\resources']

ignore_extensions = ['.cpp','.sln','.vcxproj','.filters','.user', '.config', '.cs', '.csproj']

def list_files(path):
    # Create a list to store file information
    file_list = []
    
    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(path):
        for file in files:
            # Extract file name, relative path, and extension
            file_name = file
            relative_path = os.path.relpath(root, path_to_repos)
            file_extension = os.path.splitext(file)[1]
            file_size = os.path.getsize(os.path.join(root, file))
            
            # Append file information to the list if the extension is on blacklist
            if (file_extension not in ignore_extensions):
                file_list.append((relative_path, file_name, file_extension if file_extension else "-", file_size))
                print(f"'{file}' found")
        break
    return file_list

# Specify the CSV file path to save the data
csv_file = "sample_test_files_info.csv"

# Write the file information to a CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Relative Path', 'File Name', 'File Extension', 'File Size'])
    for path in sample_assets_dirs:
        writer.writerows(list_files(path))

print(f"Output saved successfully to '{csv_file}'.")
