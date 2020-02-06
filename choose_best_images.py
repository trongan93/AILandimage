import csv, shutil
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
        if line["downloaded_path"] != None and line["downloaded_path"] != '' and line["downloaded_path"] != "NODATA":
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

            paths_to_be_kept = []
            paths_to_be_kept.append(paths[cloudcover_percent_min_index])
            paths.pop(cloudcover_percent_min_index)
            print(paths_to_be_kept)

            print('Removing useless images...')
            for path in paths:
                if path:
                    shutil.rmtree(path)
            print('All useless images removed')
            line["downloaded_path"] = '%s;' % paths_to_be_kept[0]
        
        with open(inputf, "a") as a:
            writer = csv.writer(a)
            writer.writerow(line.values())
