from utilities.image_pre import *
import matplotlib.pyplot as plt
import cv2

# path_imgs_folder = "/mnt/d/ProjectData/Landsat/Images/040034/2019-08-11/LC08/CLOUDCOVER"
path_imgs_folder = "/mnt/d/ProjectData/Landsat/tmp/LC08_L1TP_117043_20191213_20191213_01_RT"
rgb_img = combine_bands(path_imgs_folder)
plt.imshow(rgb_img)
plt.show()
# cv2.imshow("Output",rgb_img)
# cv2.waitKey(0)
# print(rgb_img)

