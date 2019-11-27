from download_landsat_scene import *
from constants import *

def main():
    inputf = INPUT_FILE_PATH

    with open(inputf, "r") as f:
        input_csv = csv.DictReader(f, delimiter=',')

        os.remove(inputf)

        # create csv header
        with open(inputf, 'a') as a:
            writer = csv.writer(a)
            writer.writerow(['lat','lng','start_date','end_date','cloudcover','satellite','station','downloaded_path'])
        
        for line in input_csv:
            result = download_scene(inputf, line)

            if str(result) != '0':
                line["downloaded_path"] = result

            with open(inputf, "a") as a:
                writer = csv.writer(a)
                writer.writerow(line.values())
                
        # with open(backupf, 'a') as backup:
        #     writer = csv.writer(backup)
        #     writer.writerow(line.values())

        ### Created by trongan93 Nov 27th
        ### Read csv file after downloaded, check field size and call crop_image.py function. Central of crop_image is lat,lng, size of crop image is depended on size in input file.
        
        



if __name__ == "__main__":
    main()  