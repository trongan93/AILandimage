import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import rasterio

def combine_bands(imgs_folder_path):
    imgs = load_images_from_folder(imgs_folder_path)
    return imgs
def read_img_by_rasterio(folder, filename):
    dataset = rasterio.open(os.path.join(folder,filename))
    return dataset

def load_images_from_folder(folder):
    global blue_img, green_img, red_img
    for filename in os.listdir(folder):
        band_name = file_name_band(filename)
        if band_name == "B2":
            blue_img = cv2.imread(os.path.join(folder,filename),0)
            blue_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
            blue_dataset = read_img_by_rasterio(folder, filename)
            print("blue dataset witdth: ", blue_dataset.width)
            print("blue dataset transform: \n", blue_dataset.transform)
            print("blue dataset bound: ", blue_dataset.bounds)
            print("Coordinate reference system (CRS): ", blue_dataset.crs)
            print("dataset indexes: ", blue_dataset.indexes)

        elif band_name == "B3":
            green_img = cv2.imread(os.path.join(folder,filename),0)
            green_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
            green_dataset = read_img_by_rasterio(folder, filename)
        elif band_name == "B4":
            red_img = cv2.imread(os.path.join(folder,filename),0)
            red_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
            red_dataset = read_img_by_rasterio(folder, filename)

    # if(blue_img == green_img):
    #     print("blue img and green img is equally")
    # plt.imshow(blue_img,cmap="gray")
    # plt.title("Blue channel - B2")
    # plt.show()
    # plt.imshow(green_img,cmap="gray")
    # plt.title("Green channel - B3")
    # plt.show()
    # plt.imshow(red_img,cmap="gray")
    # plt.title("Red channel - B4")
    # plt.show()
    rgb_img = cv2.merge([red_img,green_img,blue_img])
    return rgb_img

def file_name_band(_filename):
    file_name, file_extension = os.path.splitext(_filename)
    # print(file_name)
    # print(file_extension)
    name_parts = file_name.split('_')
    band_name = name_parts[len(name_parts)-1]
    # print(band_name)
    return band_name