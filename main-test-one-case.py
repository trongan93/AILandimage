from download_landsat_scene import *
from crop_image import *
from constants import *
from utilities.image_pre import *
from utilities.raw_image_file_data import *
import imageio
satellite = "LC8"
if satellite == "LC8":
    band_to_crop = ("B2.TIF", "B3.TIF", "B4.TIF") # B, G, R
# dir = "/mnt/d/ProjectData/CubeSAT/test-data/LC08_L1TP_141041_20130915_20170502_01_T1" #on local computer - viplab
dir = "/mnt/d/ProjectData/Landsat/LandslideTest/LC08_L1TP_141041_20140918_20170419_01_T1" #on viplab-server1
# dir = "/mnt/d/Landsat/LandslideTest/LC08_L1TP_141041_20130915_20170502_01_T1" #run on local
size = 'CNN_FIX' #'VERY_LARGE'
# size = 'VERY_LARGE'
lng = '85.868467'
lat = '27.770733'

if not(os.path.exists(dir)):
    print('dir not exists')

cropped_folder = ""

before_cropped = FileRawData(dir)
before_cropped_image = combine_bands(dir, satellite)
before_cropped_image = automatic_brightness_and_contrast(before_cropped_image)

before_cropped.save_feature_raw_image('before_cropped', before_cropped_image)
plt.imshow(before_cropped_image)
plt.show()

before_read_img = before_cropped.read_feature_raw_image('before_cropped', before_cropped_image.shape)
# plt.imshow(read_img)
# plt.show()

filepath = os.path.join(dir, 'before_cropped')
imageio.imsave(filepath + '.TIF', before_read_img)

band_files = []
is_out_of_range = False
for filename in os.listdir(dir):
    # print(filename)
    if filename.endswith(band_to_crop):
        filepath = os.path.join(dir, filename)
        rgb_img = crop_image_based_on_impact(filepath, size, lng, lat)

        if (rgb_img.size != 0):
            cropped_folder = os.path.join(dir, "cropped")
            makedir_if_path_not_exists(cropped_folder)
            band_files.append(os.path.join(cropped_folder, f'cropped_{size}_{filename}'))

            cv2.imwrite(os.path.join(cropped_folder, f'cropped_{size}_{filename}'), rgb_img)
        else:
            is_out_of_range = True
            break

if (is_out_of_range):
    dir = os.path.join(dir, "error", "latlng_out_of_range")
    final_paths.append(dir)
    print('lat and lng out of range')

rgb_img = combine_bands(cropped_folder, satellite)
rgb_img = rgb_img + 60
try:
    rgb_img = automatic_brightness_and_contrast(rgb_img)
except:
    if float(line["cloudcover"]) > 90:
        print("Cloudcover too high, remove images")
        shutil.rmtree(dir)
    else:
        print("Something wrong")

plt.imshow(rgb_img, origin='lower')
plt.show()

filename = f'{float(lat)}_{float(lng)}_{size}_cropped'
filepath = os.path.join(cropped_folder, filename)
raw_data = FileRawData(cropped_folder)
raw_data.save_feature_raw_image(filename, rgb_img)

# cv2.imwrite(filepath, rgb_img)
read_img = raw_data.read_feature_raw_image(filename, rgb_img.shape)
# plt.imshow(read_img)
# plt.show()

imageio.imsave(filepath + '.TIF', read_img)

# for band in band_files:
#     os.remove(band)
# final_paths.append(dir)
# if final_paths == []:
# line["downloaded_path"] = "NODATA"
# else:
# line["downloaded_path"] = ';'.join(final_paths) + ";"
# with open(inputf, "a") as a:
# writer = csv.writer(a)
# writer.writerow(line.values())