import csv, shutil
from constants import *
from utilities.directory_helper import *

def choose_best_image(paths, cloudcover_percent):
    """
        Given the PATHS for downloaded images and the threshold cloudcover percent, find the path to the image with minium cloudcover
        Parameters:
        paths: string
        cloudcover_percent: float
    """
    cloudcover_percent_min_index = 0
    paths = str(paths).split(';')
    for (index, path) in enumerate(paths):
        path_arr = split_all(path)
        if path_arr:
            print(path_arr)
            if float(path_arr[0]) < cloudcover_percent:
                cloudcover_percent = float(path_arr[0])
                cloudcover_percent_min_index = index
    # print(cloudcover_percent)
    # print(cloudcover_percent_min_index)
    return paths[cloudcover_percent_min_index]

def choose_best_images_csv(csv_file_path=INPUT_FILE_PATH):
    """
    Choose best images for each record in csv data
    Parameters:
    csv_file_path: string
    Return a dictionary that consist of ID of record and the best image found for that record (some of the records in csv does not have data)
    """
    inputf = csv_file_path
    best_images_in_csv = {}
    with open(inputf, "r") as f:
        input_csv = csv.DictReader(f, delimiter=',')

        for line in input_csv:
            if line["downloaded_path"] != None and line["downloaded_path"] != '' and line["downloaded_path"] != "NODATA":
                # print(line)
                cloudcover_percent = float(line["cloudcover"])
                best_image = choose_best_image(line["downloaded_path"], cloudcover_percent)

                best_images_in_csv[line["id"]] = best_image
                # line["downloaded_path"] = '%s;' % best_image
    
    return best_images_in_csv

### Test function
# best_images_in_csv = choose_best_images_csv()
# for idx, path in best_images_in_csv.items():
#     print("Id: ", idx)
#     print("Path: ", path)
