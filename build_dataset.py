import csv, shutil
def change_path_in_dataserver(downloaded_img_path):
    if(downloaded_img_path != None and downloaded_img_path != '' and downloaded_img_path != 'NODATA'):
        path_members = downloaded_img_path.split('/')
        # print('old path: ', downloaded_img_path)
        new_path = path_members[0] + '/' + path_members[1] + '/' + path_members[2] + '/' + path_members[4] + '/' + path_members[5] + '/' + path_members[6] + '/' + path_members[7] + '/' + path_members[8] + '/' + path_members[9] + '/' + 'cropped'
        # print('new path: ', new_path)
        return new_path

def merge_image_to_dataset(csv_file_path, landslide_dataset_path):
    inputf = csv_file_path
    with open(inputf,"r") as f:
        input_csv = csv.DictReader(f, delimiter=',')

        for line in input_csv:
            downloadedpath = line["downloaded_path"]
            downloadedpath_members = downloadedpath.split(';')
            for downloaded_img_path in downloadedpath_members:
                path_in_data_server = change_path_in_dataserver(downloaded_img_path)
                shutil.copytree(path_in_data_server, landslide_dataset_path)

            # print(downloadedpath_members[0])

# Run on Data server at viplab3
merge_image_to_dataset("/mnt/d/LandslideData/Landsat/input_0_280.csv", "/mnt/d/LandslideData/Landsat/")
merge_image_to_dataset("/mnt/d/LandslideData/Landsat/input_281_560.csv", "/mnt/d/LandslideData/Landsat/")