import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import rasterio

def combine_bands(imgs_folder_path, satellite):
    imgs = load_images_from_folder(imgs_folder_path, satellite)
    return imgs
def read_img_by_rasterio(folder, filename):
    dataset = rasterio.open(os.path.join(folder,filename))
    return dataset

def load_images_from_folder(folder, satellite):
    global blue_img, green_img, red_img
    if satellite == "LC8":
        for filename in os.listdir(folder):
            band_name = file_name_band(filename)
            if band_name == "B2":
                blue_img = cv2.imread(os.path.join(folder,filename),0)
                blue_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                blue_dataset = read_img_by_rasterio(folder, filename)
                print("img shape: ", blue_img.shape)
                # print("blue dataset witdth: ", blue_dataset.width)
                # print("blue dataset transform: \n", blue_dataset.transform)
                # print("blue dataset bound: ", blue_dataset.bounds)
                # print("Coordinate reference system (CRS): ", blue_dataset.crs)
                # print("dataset indexes: ", blue_dataset.indexes)

            elif band_name == "B3":
                green_img = cv2.imread(os.path.join(folder,filename),0)
                green_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                green_dataset = read_img_by_rasterio(folder, filename)
            elif band_name == "B4":
                red_img = cv2.imread(os.path.join(folder,filename),0)
                red_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                red_dataset = read_img_by_rasterio(folder, filename)
    elif satellite == "LE7":
        for filename in os.listdir(folder):
            band_name = file_name_band(filename)
            if band_name == "B1":
                blue_img = cv2.imread(os.path.join(folder,filename),0)
                blue_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                blue_dataset = read_img_by_rasterio(folder, filename)
                print("img shape: ", blue_img.shape)
                # print("blue dataset witdth: ", blue_dataset.width)
                # print("blue dataset transform: \n", blue_dataset.transform)
                # print("blue dataset bound: ", blue_dataset.bounds)
                # print("Coordinate reference system (CRS): ", blue_dataset.crs)
                # print("dataset indexes: ", blue_dataset.indexes)

            elif band_name == "B2":
                green_img = cv2.imread(os.path.join(folder,filename),0)
                green_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                green_dataset = read_img_by_rasterio(folder, filename)
            elif band_name == "B3":
                red_img = cv2.imread(os.path.join(folder,filename),0)
                red_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                red_dataset = read_img_by_rasterio(folder, filename)
    elif satellite == "LT5":
        for filename in os.listdir(folder):
            band_name = file_name_band(filename)
            if band_name == "B1":
                blue_img = cv2.imread(os.path.join(folder,filename),0)
                blue_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                blue_dataset = read_img_by_rasterio(folder, filename)
                print("img shape: ", blue_img.shape)
                # print("blue dataset witdth: ", blue_dataset.width)
                # print("blue dataset transform: \n", blue_dataset.transform)
                # print("blue dataset bound: ", blue_dataset.bounds)
                # print("Coordinate reference system (CRS): ", blue_dataset.crs)
                # print("dataset indexes: ", blue_dataset.indexes)

            elif band_name == "B2":
                green_img = cv2.imread(os.path.join(folder,filename),0)
                green_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                green_dataset = read_img_by_rasterio(folder, filename)
            elif band_name == "B3":
                red_img = cv2.imread(os.path.join(folder,filename),0)
                red_np = np.fromfile(os.path.join(folder,filename),dtype='uint8')
                red_dataset = read_img_by_rasterio(folder, filename)
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

# Automatic brightness and contrast optimization with optional histogram clipping
#Ref: https://stackoverflow.com/questions/56905592/automatic-contrast-and-brightness-adjustment-of-a-color-photo-of-a-sheet-of-pape/56909036
def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    print("Automatic brightness and contrast")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    if(maximum_gray - minimum_gray == 0):
        return image
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    print("alpha: ", alpha, ", beta: ", beta)
    # return (auto_result, alpha, beta)
    return auto_result