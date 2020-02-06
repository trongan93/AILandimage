from download_landsat_scene import *
from crop_image import *
from constants import *
from utilities.image_pre import *

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
                count += 1

                with open(inputf, "a") as a:
                    writer = csv.writer(a)
                    writer.writerow(line.values())
     ### Created by trongan93 Nov 27th
        ### Read csv file after downloaded, check field size and call crop_image.py function. Central of crop_image is lat,lng, size of crop image is depended on size in input file.
    elif choice == 2:
        with open(inputf, 'r') as f:
            input_csv = csv.DictReader(f, delimiter=',')
            for line in input_csv:
                lat = float(line["lat"])
                lng = float(line["lng"])
                size = str(line["size"])
                downloaded_path = str(line["downloaded_path"])

                if downloaded_path == None or downloaded_path == "" or downloaded_path == "NODATA":
                    continue

                dirs = downloaded_path.split(';')
                
                save_file_extension = "jpg"
                band_to_crop = ("B2.TIF", "B3.TIF", "B4.TIF") # B, G, R
                for dir in dirs:
                    cropped_folder = ""
                    for filename in os.listdir(dir):
                        print(filename)
                        if filename.endswith(band_to_crop):
                            filepath = os.path.join(dir, filename)
                            rgb_img = crop_image_based_on_impact(filepath, size, lng, lat)

                            cropped_folder = os.path.join(dir, "cropped")
                            makedir_if_path_not_exists(cropped_folder)

                            cv2.imwrite(os.path.join(cropped_folder, f'cropped_{size}_{filename}'), rgb_img)

                    rgb_img = combine_bands(cropped_folder)
                    rgb_img = rgb_img + 60
                    rgb_img = automatic_brightness_and_contrast(rgb_img)
                    plt.imshow(rgb_img)
                    plt.show()
                    filename = os.path.join(cropped_folder, f'{size}_cropped.{save_file_extension}')
                    cv2.imwrite(filename, rgb_img)



        



if __name__ == "__main__":
    # 1 for downloading new landsat data
    # 2 for cropping and combining image
    main(sys.argv[1])  