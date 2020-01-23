from download_landsat_scene import *
from crop_image import *
from constants import *

def main():
    inputf = INPUT_FILE_PATH

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
        with open(inputf, 'r') as f:
            input_csv = csv.DictReader(f, delimiter=',')
            for line in input_csv:
                lat = float(line["lat"])
                lng = float(line["lng"])
                size = str(line["size"])
                downloaded_path = str(line["downloaded_path"])

                if downloaded_path == None or downloaded_path == "":
                    continue

                dirs = downloaded_path.split(';')
                
                for dir in dirs:
                    for filename in os.listdir(dir):
                        if filename.endswith('.TIF'):
                            img = crop_image_based_on_impact(os.path.join(dir, filename), size, lng, lat)
                            
                            cv2.imwrite(filename, img)


        



if __name__ == "__main__":
    main()  