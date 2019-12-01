import csv
from constants import *
from utilities.directory_helper import *

inputf = INPUT_FILE_PATH
with open(inputf, "r") as f:
    input_csv = csv.DictReader(f, delimiter=',')
    os.remove(inputf)

    # create csv header
    with open(inputf, 'a') as a:
        writer = csv.writer(a)
        writer.writerow(['id','lat','lng','start_date','end_date','size','cloudcover','satellite','station','downloaded_path'])

    for line in input_csv:
        if line["downloaded_path"] != None and line["downloaded_path"] != '':
            # print(line)
            cloudcover_percent = float(line["cloudcover"])
            cloudcover_percent_min_index = 0
            paths = str(line["downloaded_path"]).split(';')
            for (index, path) in enumerate(paths):
                path_arr = split_all(path)
                if path_arr:
                    print(path_arr)
                    if float(path_arr[0]) < cloudcover_percent:
                        cloudcover_percent = float(path_arr[0])
                        cloudcover_percent_min_index = index
            print(cloudcover_percent)
            print(cloudcover_percent_min_index)
            print(paths[cloudcover_percent_min_index])

            line["downloaded_path"] = '%s;' % paths[cloudcover_percent_min_index]
        
        with open(inputf, "a") as a:
            writer = csv.writer(a)
            writer.writerow(line.values())
