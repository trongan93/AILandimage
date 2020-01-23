from utilities.rasterio_helper import *
from enums import LANDSLIDE_IMPACT_SIZE

import matplotlib.pyplot as plt
import cv2

def get_rect(img, row, col, size=(600, 600)):
    width, height = size
    top_left_x = 0
    top_left_y = 0

    if col >= (width // 2):
        top_left_x = (col - width // 2)
    if row >= (height // 2):
        top_left_y = (row - height // 2)

    return img[top_left_y:top_left_y+height, top_left_x:top_left_x+width]

def get_impact_size(impact):
    impact = impact.upper()
    return LANDSLIDE_IMPACT_SIZE[impact].value

def crop_image_based_on_impact(path, impact, lng, lat):
    img = cv2.imread(path)
    row, col = lnglat_to_image_coors(path, lng, lat)
    
    if row < 0 or row > img.shape[0] or col < 0 or col > img.shape[1]:
        print("Lat lng out of range")
        return

    print("Row: ", row)
    print("Col: ", col)
    print("Pixel value: ", img[row][col])

    impact_size = get_impact_size(impact)    
    img = get_rect(img, row, col, impact_size)

    print(img.shape)
    plt.imshow(img)
    plt.show()

    return img

# lat 38.43660
# lon -117.29791
# crop_image_based_on_impact("/home/trainer1234/research/trunk/040034/2011-02-10/LT05/CLOUDCOVER/LT05_L1TP_040034_20110210_20160901_01_T1_B1.TIF", "VERY_LARGE", -116, 37)