import pandas as pd
import geopy
from geopy.distance import VincentyDistance
from constants import RANDOM_DISTANCE_FROM_LANDSLIDE_POINT as random_distances
from constants import RANDOM_DISTANCE_BEARING_FROM_LANDSLIDE_POINT as random_bearings
from utilities.raw_image_file_data import *
from utilities.image_pre import *
from crop_image import *
from download_landsat_scene import *
import imageio
import matplotlib.pyplot as plt
import shutil

def create_negative_landslide(inputf):
    # ref: https://stackoverflow.com/questions/4530943/calculating-a-gps-coordinate-given-a-point-bearing-and-distance/4531227#4531227
    print('filename: ', inputf)
    data1 = pd.read_csv(inputf)
    # print('keys: ', data1.keys())

    for index, row in data1.iterrows():
        landslide_point = geopy.Point(row['lat'],row['lng'])
        satellite = str(row["satellite"])
        downloaded_path = row['downloaded_path']
        if downloaded_path == None or downloaded_path == "" or downloaded_path == "NODATA" or downloaded_path.strip() == "" or (
                "EXCEPTION" in downloaded_path.upper()):
            print("Download path error at index: ", index)
            continue
        dirs = downloaded_path.split(';')
        dirs.remove('')

        random_withoutlandslide_points = []
        for random_dist in random_distances:
            for random_bearing in random_bearings:
                new_point = VincentyDistance(kilometers=random_dist).destination(landslide_point, random_bearing)
                random_withoutlandslide_points.append(new_point)
                # print('new point lat: ', new_point.latitude, ' , origin lng: ', new_point.longitude)
        # print('size of random points is ', len(random_withoutlandslide_points))

        for dir in dirs:
            crop_status = crop_new_negative_img(dir, random_withoutlandslide_points, satellite)
            if crop_status != 1:
                print('Failed to created negative landslide region on: ', dir)







def crop_new_negative_img(dir, nolandslidepoints, satellite):
    bandToCrop = ("B2.TIF", "B3.TIF", "B4.TIF")  # B, G, R
    if satellite == "LE7":
        bandToCrop = ("B1.TIF", "B2.TIF", "B3.TIF")
    elif satellite == "LT5":
        bandToCrop = ("B1.TIF", "B2.TIF", "B3.TIF")
    elif satellite == "LC8":
        bandToCrop = ("B2.TIF", "B3.TIF", "B4.TIF")  # B, G, R

    img_size = "CNN_FIX"
    band_files = []
    for index, nolandslidepoint in enumerate(nolandslidepoints):
        for filename in os.listdir(dir):
            if filename.endswith(bandToCrop):
                filepath = os.path.join(dir, filename)
                band_croped = crop_image_based_on_impact(filepath, img_size, nolandslidepoint.longitude, nolandslidepoint.latitude)
                if(band_croped.size != 0):
                    negative_cropped_folder = os.path.join(dir,"negative_cropped")
                    makedir_if_path_not_exists(negative_cropped_folder)
                    negative_cropped_folder_tmp = os.path.join(negative_cropped_folder,"tmp")
                    makedir_if_path_not_exists(negative_cropped_folder_tmp)
                    imageio.imsave(os.path.join(negative_cropped_folder_tmp,f'negative_{index}_{img_size}_{filename}'),band_croped)
                    band_files.append(os.path.join(negative_cropped_folder_tmp,f'negative_{index}_{img_size}_{filename}'))
        if(len(band_files)>0):
            rgb_nolandslide = combine_bands(negative_cropped_folder_tmp,satellite)
            rgb_nolandslide = rgb_nolandslide + 60
            rgb_nolandslide = automatic_brightness_and_contrast(rgb_nolandslide)
            rgb_cropped_file_name = f'lat_{nolandslidepoint.latitude}_lng_{nolandslidepoint.longitude}_cropped'
            rgb_cropped_file_path = os.path.join(negative_cropped_folder,rgb_cropped_file_name + '.TIF')
            imageio.imsave(rgb_cropped_file_path, rgb_nolandslide)
            plt.imshow(rgb_nolandslide)
            plt.show()
            print('successfully to create a no landslide image at lat: ', nolandslidepoint.latitude, ' and lng: ', nolandslidepoint.longitude)
            for band_file in band_files:
                if(os.path.exists(band_file)):
                    os.remove(band_file)
            if remove_folder(negative_cropped_folder_tmp) == 1:
                print('sucessfully to remove: ', negative_cropped_folder_tmp)

        band_files.clear()
    return 1

def remove_folder(folder_path):
    if (os.path.exists(folder_path)):
        filesInPath = os.listdir(folder_path)
        for f1 in filesInPath:
            os.remove(os.path.join(folder_path,f1))
        os.rmdir(folder_path)
    return 1