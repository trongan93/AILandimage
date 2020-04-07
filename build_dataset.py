import csv, shutil, os

def change_path_in_dataserver(downloaded_img_path):
    if(downloaded_img_path != None and downloaded_img_path.strip() != '' and downloaded_img_path != 'NODATA') and not("EXCEPTION" in downloaded_path.upper()) and not("ERROR" in downloaded_path.upper()):
        path_members = downloaded_img_path.split(os.sep)
        # print('old path: ', downloaded_img_path)
        new_path = path_members[0] + '/' + path_members[1] + '/' + path_members[2] + '/' + path_members[4] + '/' + path_members[5] + '/' + path_members[6] + '/' + path_members[7] + '/' + path_members[8] + '/' + path_members[9] + '/' + 'cropped/'
        # print('new path: ', new_path)
        return new_path

def safe_copy(source, destination):
    """
        Safely copy file from source to destination. If a file with the same name already exists, the destination path is changed to preserve both
    """
    if os.path.exists(destination):
        base, extension = os.path.splitext(destination)
        index = 1
        destination = os.path.exists(f'{base}_{index}{extension}')
        while os.path.exists(destination):
            index += 1
            destination = os.path.exists(f'{basename}_{index}{extension}')
    
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
                img_files = os.listdir(path_in_data_server)
                if(len(img_files) > 0):
                    for f in img_files:
                        img_path = str(path_in_data_server) + f
                        print(img_path)
                        dest_path = os.path.join(landslide_dataset_path, f)

                        safe_copy(img_path, dest_path)
                        
                        

            # print(downloadedpath_members[0])

# Run on Data server at viplab3
# merge_image_to_dataset("/home/trongan93/Desktop/input_0_280.csv", "/mnt/d/LandslideData/Landsat/")
merge_image_to_dataset("/mnt/d/LandslideData/input_0_280.csv", "/mnt/d/LandslideData/Landsat/")
merge_image_to_dataset("/mnt/d/LandslideData/input_281_560.csv", "/mnt/d/LandslideData/Landsat/")