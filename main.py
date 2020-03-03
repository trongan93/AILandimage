from download_landsat_scene import *
from crop_image import *
from constants import *
from utilities.image_pre import *
from utilities.raw_image_file_data import *

import imageio

def main(choice):
    inputf = INPUT_FILE_PATH
    choice = int(choice)
    ### Download landsat scene
    if choice == 1:
        with open(inputf, "r") as f:
            input_csv = csv.DictReader(f, delimiter=',')

            os.remove(inputf)

            # create csv header
            with open(inputf, 'a') as a:
                writer = csv.writer(a)
                writer.writerow(['id','lat','lng','start_date','end_date','size','cloudcover','satellite','station','downloaded_path'])
            
            count = 0
            for line in input_csv:
                result = download_scene(inputf, line)

                if str(result) != '0':
                    line["downloaded_path"] = result

                line["id"] = count
                # count += 1

                with open(inputf, "a") as a:
                    writer = csv.writer(a)
                    writer.writerow(line.values())
     ### Created by trongan93 Nov 27th
        ### Read csv file after downloaded, check field size and call crop_image.py function. Central of crop_image is lat,lng, size of crop image is depended on size in input file.
    elif choice == 2:
        with open(inputf, 'r') as f:
            input_csv = csv.DictReader(f, delimiter=',')
            os.remove(inputf)

            # create csv header
            with open(inputf, 'a') as a:
                writer = csv.writer(a)
                writer.writerow(['id','lat','lng','start_date','end_date','size','cloudcover','satellite','station','downloaded_path'])

            for line in input_csv:
                lat = float(line["lat"])
                lng = float(line["lng"])
                size = str(line["size"])
                satellite = str(line["satellite"])
                downloaded_path = str(line["downloaded_path"])

                if downloaded_path == None or downloaded_path == "" or downloaded_path == "NODATA":
                    with open(inputf, "a") as a:
                        writer = csv.writer(a)
                        writer.writerow(line.values())
                    continue

                dirs = downloaded_path.split(';')
                dirs.remove('')
                band_to_crop = ("B2.TIF", "B3.TIF", "B4.TIF") # B, G, R
                if satellite == "LE7":
                    band_to_crop = ("B1.TIF", "B2.TIF", "B3.TIF")
                elif satellite == "LT5":
                    band_to_crop = ("B1.TIF", "B2.TIF", "B3.TIF")
                elif satellite == "LC8":
                    band_to_crop = ("B2.TIF", "B3.TIF", "B4.TIF") # B, G, R
                final_paths = []
                for dir in dirs:
                    if not(os.path.exists(dir)):
                        continue

                    cropped_folder = ""
                    
                    before_cropped = FileRawData(dir)
                    before_cropped_image = combine_bands(dir, satellite)
                    before_cropped_image = automatic_brightness_and_contrast(before_cropped_image)
                    
                    before_cropped.save_feature_raw_image('before_cropped', before_cropped_image)
                    # # plt.imshow(before_cropped_image)
                    # # plt.show()

                    before_read_img = before_cropped.read_feature_raw_image('before_cropped', before_cropped_image.shape)
                    # plt.imshow(read_img)
                    # plt.show()

                    filepath = os.path.join(dir, 'before_cropped')
                    imageio.imsave(filepath + '.TIF', before_read_img)

                    band_files = []
                    for filename in os.listdir(dir):
                        # print(filename)
                        if filename.endswith(band_to_crop):
                            filepath = os.path.join(dir, filename)
                            rgb_img = crop_image_based_on_impact(filepath, size, lng, lat)

                            cropped_folder = os.path.join(dir, "cropped")
                            makedir_if_path_not_exists(cropped_folder)
                            band_files.append(os.path.join(cropped_folder, f'cropped_{size}_{filename}'))

                            cv2.imwrite(os.path.join(cropped_folder, f'cropped_{size}_{filename}'), rgb_img)
                    
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
                        continue
                    # plt.imshow(rgb_img)
                    # plt.show()
                    
                    filename = f'{int(lat)}_{int(lng)}_{size}_cropped'
                    filepath = os.path.join(cropped_folder, filename)
                    raw_data = FileRawData(cropped_folder)
                    raw_data.save_feature_raw_image(filename, rgb_img)

                    # cv2.imwrite(filepath, rgb_img)
                    read_img = raw_data.read_feature_raw_image(filename, rgb_img.shape)
                    # plt.imshow(read_img)
                    # plt.show()

                    imageio.imsave(filepath + '.TIF', read_img)

                    for band in band_files:
                        os.remove(band)
                    final_paths.append(dir)
                if final_paths == []:
                    line["downloaded_path"] = "NODATA"
                else:
                    line["downloaded_path"] = ';'.join(final_paths) + ";"
                with open(inputf, "a") as a:
                    writer = csv.writer(a)
                    writer.writerow(line.values())
        



if __name__ == "__main__":
    # 1 for downloading new landsat data
    # 2 for cropping and combining image
    main(sys.argv[1])  