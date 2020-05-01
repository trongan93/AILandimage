from download_landsat_scene import *
from constants import *
from utilities.convertor import *
from utilities.parser import *
from collections import OrderedDict

def sync_landslidedata_to_input_csv(first_sync = False):
    """
        Sync data in landslidedata.csv to input.csv
        * @param first_sync=True for first sync
        * first_sync=False for appending new record from landslidedata.csv to input.csv
    """
    inputf = INPUT_FILE_PATH
    landslide_data_file = LANDSLIDE_DATA_FILE_PATH

    count = 0
    if (not(first_sync)):
        with open(inputf, "r") as inpf:
            rows = list(csv.DictReader(inpf, delimiter=','))
            count = int(rows[-1]["id"])
    
    with open(landslide_data_file, "r") as f2:
        landslide_data = csv.DictReader(f2, delimiter=',')
        
        for data in landslide_data:
            if (not(first_sync)):
                # skip processed rows
                if int(data["OBJECTID"]) <= count:
                    continue
                count += 1
            
            with open(inputf, "a") as inpf:
                for satellite in ['LC8', 'LE7', 'LT5']:
                    line = OrderedDict()
                    line['id'] = count
                    line['lat'] = data['latitude']
                    line['lng'] = data['longitude']

                    if not(data['date_']): 
                        continue
                    date_ = utc_to_normal_date(data['date_'])
                    start_date = parse_date(date_)
                    end_date = start_date + datetime.timedelta(days=91)

                    line['start_date'] = date_
                    line['end_date'] = convert_date_to_normal_date_str(end_date)
                    
                    line['size'] = data['landslide1']
                    line['cloudcover'] = '100'
                    line['satellite'] = satellite
                    line['station'] = 'ALL'
                    line["downloaded_path"] = ''

                    # print(line)
                    writer = csv.writer(inpf)
                    writer.writerow(line.values())

                    if(first_sync): count += 1
    
    print("All records synced")

if __name__ == "__main__":
    sync_landslidedata_to_input_csv(True)  
