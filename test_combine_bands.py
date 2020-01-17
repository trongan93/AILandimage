from utilities.image_pre import *
import matplotlib.pyplot as plt
import cv2

# path_imgs_folder = "/mnt/d/ProjectData/Landsat/Images/040034/2019-08-11/LC08/CLOUDCOVER"
# path_imgs_folder = "/mnt/d/ProjectData/Landsat/tmp/LC08_L1TP_117043_20191213_20191213_01_RT"
path_imgs_folder = "/mnt/d/ProjectData/Landsat/tmp/LC08_L1TP_141041_20140918_20170419_01_T1_Sunkosi_Landslide"
rgb_img = combine_bands(path_imgs_folder)
rgb_img = rgb_img + 60
plt.imshow(rgb_img)
plt.show()

# new_rgb = change_contract_and_bright(rgb_img)
new_rgb_2 = automatic_brightness_and_contrast(rgb_img)
plt.imshow(new_rgb_2)
plt.show()

# cv2.imshow("Output",rgb_img)
# cv2.waitKey(0)
# print(rgb_img)

