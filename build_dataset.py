import csv, shutil, os

def change_path_in_dataserver(downloaded_img_path, negative_landslide = 0):
    if(downloaded_img_path != None and downloaded_img_path.strip() != '' and downloaded_img_path != 'NODATA' and not("EXCEPTION" in downloaded_img_path.upper()) and not("ERROR" in downloaded_img_path.upper())):
        path_members = downloaded_img_path.split(os.sep)
        # print('old path: ', downloaded_img_path)
        if negative_landslide == 0:
            new_path = path_members[0] + '/' + path_members[1] + '/' + path_members[2] + '/' + path_members[4] + '/' + path_members[5] + '/' + path_members[6] + '/' + path_members[7] + '/' + path_members[8] + '/' + path_members[9] + '/' + 'cropped/'
        else:
            new_path = os.path.join(downloaded_img_path,'negative_cropped/')
            print('new path: ', new_path)
        return new_path

def safe_copy(source, destination):
    """
        Safely copy file from source to destination. If a file with the same name already exists, the destination path is changed to preserve both
    """
    if os.path.exists(destination):
        base, extension = os.path.splitext(destination)
        index = 1
        destination = f'{base}_{index}{extension}'
        while os.path.exists(destination):
            index += 1
            destination = f'{base}_{index}{extension}'
    
    shutil.copy(source, destination)

def merge_image_to_dataset(csv_file_path, landslide_dataset_path):
    inputf = csv_file_path
    with open(inputf,"r") as f:
        input_csv = csv.DictReader(f, delimiter=',')

        for line in input_csv:
            downloadedpath = line["downloaded_path"]
            downloadedpath_members = downloadedpath.split(';')

            for downloaded_img_path in downloadedpath_members:
                path_in_data_server = change_path_in_dataserver(downloaded_img_path)
                
                if not(path_in_data_server):
                    continue

                img_files = os.listdir(path_in_data_server)
                if(len(img_files) > 0):
                    for f in img_files:
                        img_path = str(path_in_data_server) + f
                        print(img_path)
                        dest_path = os.path.join(landslide_dataset_path, f)

                        safe_copy(img_path, dest_path)
                        
                        

            # print(downloadedpath_members[0])

def merge_negative_landslide_image_to_dataset(csv_file_path, landslide_dataset_path):
    inputf = csv_file_path
    with open(inputf, "r") as f:
        input_csv = csv.DictReader(f, delimiter=',')

        for line in input_csv:
            downloadedpath = line["downloaded_path"]
            downloadedpath_members = downloadedpath.split(';')

            for downloaded_img_path in downloadedpath_members:
                path_in_data_server = change_path_in_dataserver(downloaded_img_path, 1)

                if not (path_in_data_server):
                    break

                img_files = os.listdir(path_in_data_server)
                if (len(img_files) > 0):
                    for f in img_files:
                        img_path = str(path_in_data_server) + f
                        print(img_path)
                        dest_path = os.path.join(landslide_dataset_path, f)

                        safe_copy(img_path, dest_path)

def remove_raw_ext(directory_path):
    files_in_directory = os.listdir(directory_path)
    filtered_files = [file for file in files_in_directory if file.endswith(".raw")]
    for file in filtered_files:
        path_to_file = os.path.join(directory_path, file)
        os.remove(path_to_file)

def random_selected_negative(full_directory_path, selected_random_directory_path):
    files_in_directory = os.listdir(full_directory_path)
    for index, file_path in enumerate(files_in_directory):
        if index%10 == 0:
            safe_copy(os.path.join(full_directory_path,file_path),os.path.join(selected_random_directory_path,file_path))
    print("Done to random selected Negative")


# Run on Data server at viplab3
# merge_image_to_dataset("/home/trongan93/Desktop/input_0_280.csv", "/mnt/d/LandslideData/Landsat/")
# merge_image_to_dataset("/mnt/d/LandslideData/input_0_280.csv", "/mnt/d/LandslideData/Landsat/")
# merge_image_to_dataset("/mnt/d/LandslideData/input_281_560.csv", "/mnt/d/LandslideData/Landsat/")

#Negative landslide building
# merge_negative_landslide_image_to_dataset("input_0_280.csv", "/mnt/d/ProjectData/NegativeLandslideData/Landsat/")
# merge_negative_landslide_image_to_dataset("input_281_560.csv", "/mnt/d/ProjectData/NegativeLandslideData/Landsat/")

#Remove raw files in dataset
# remove_raw_ext('/mnt/d/ProjectData/SatelliteDataset/Landslide/Positive')

#Random Negative images selected
random_selected_negative("/mnt/d/ProjectData/SatelliteDataset/Landslide/Negative","/mnt/d/ProjectData/SatelliteDataset/Landslide/Negative_Selected")
