import csv
from constants import *
from utilities.convertor import *
from utilities.parser import *
from collections import OrderedDict
from abc import ABC, abstractmethod
import os

class AInputCsvDataBuilder(ABC):
    """
    Extract necessary fields from csv scene file and move it into another input csv file for downloading scene
    """

    _inputf = INPUT_FILE_PATH
    _csv_file = ""

    def __init__(self, csv_file):
        self._csv_file = csv_file

    def __init__(self, csv_file, inputf):
        self._csv_file = csv_file
        self._inputf = inputf

    def get_csv_file_path(self):
        return self._csv_file

    def get_input_file(self):
        return self._inputf

    def build_csv_header(self, inputf):
        with open(inputf, 'r') as f:
            input_csv = csv.DictReader(f, delimiter=',')
            inputs = list(input_csv)
        os.remove(inputf)

        # create csv header
        with open(inputf, 'a') as a:
            writer = csv.writer(a)
            writer.writerow(['id','lat','lng','start_date','end_date','size','cloudcover','satellite','station','downloaded_path'])
 
    def build_input_csv_file(self):   
        input_file = self.get_input_file()
        self.build_csv_header(input_file)

        with open(self.get_csv_file_path(), "r") as f2:
            landslide_data = csv.DictReader(f2, delimiter=',')
            self.build_csv_data(landslide_data, input_file)
            
        print("All necessary fields are extracted")

    def build_csv_data(self, source_data, input_file):
        count = 0
        for data in source_data:
            with open(input_file, "a") as inpf:
                for satellite in ['LC8']:
                    line = self.extract_necessary_fields_for_download(data, satellite, count)
                    if line == None:
                        continue
                    # print(line)

                    writer = csv.writer(inpf)
                    writer.writerow(line.values())
                    count += 1

    @abstractmethod
    def extract_necessary_fields_for_download(self, source_data, satellite, count):
        pass

class LandslidedataCSVBuilder(AInputCsvDataBuilder):
    def extract_necessary_fields_for_download(self, source_data, satellite, count):
        line = OrderedDict()
        line['id'] = count
        line['lat'] = source_data['latitude']
        line['lng'] = source_data['longitude']

        if not(source_data['date_']): 
            return None
        date_ = utc_to_normal_date(source_data['date_'])
        start_date = parse_date(date_)
        end_date = start_date + datetime.timedelta(days=180)

        line['start_date'] = date_
        line['end_date'] = convert_date_to_normal_date_str(end_date)
        
        line['size'] = source_data['landslide1']
        line['cloudcover'] = '10'
        line['satellite'] = satellite
        line['station'] = 'ALL'
        line["downloaded_path"] = ''

        return line

class NasaGlobalLandslideCSVBuilder(AInputCsvDataBuilder):
    def extract_necessary_fields_for_download(self, source_data, satellite, count):
        line = OrderedDict()
        line['id'] = count
        line['lat'] = source_data['latitude']
        line['lng'] = source_data['longitude']

        if not(source_data['event_date']): 
            return None

        date_ = convert_datestr_to_normal_date(source_data['event_date'], "%Y-%m-%d %H:%M:%S")
        start_date = parse_date(date_)
        end_date = start_date + datetime.timedelta(days=180)

        line['start_date'] = date_
        line['end_date'] = convert_date_to_normal_date_str(end_date)
        
        line['size'] = source_data['landslide_size']
        line['cloudcover'] = '10'
        line['satellite'] = satellite
        line['station'] = 'ALL'
        line["downloaded_path"] = ''

        return line

class InputCSVFactory():
    _inputf = INPUT_FILE_PATH
    _file_type = ""
    _csv_file = ""

    def __init__(self, csv_file, file_type):
        self._csv_file = csv_file
        self._file_type = file_type

    def __init__(self, csv_file, inputf, file_type):
        self._csv_file = csv_file
        self._inputf = inputf
        self._file_type = file_type

    def get_csv_file_path(self):
        return self._csv_file

    def get_input_file(self):
        return self._inputf
    
    def get_file_type(self):
        return self._file_type

    def create_csv_builder(self):
        file_type = self.get_file_type()
        source_csv_path = self.get_csv_file_path()

        if file_type == "LANDSLIDE":
            return LandslidedataCSVBuilder(source_csv_path, self.get_input_file())
        elif file_type == "NASA_GLOBAL_LANDSLIDE":
            return NasaGlobalLandslideCSVBuilder(source_csv_path, self.get_input_file())
        else:
            print("Wrong type")
            return None


if __name__ == "__main__":
    factory = InputCSVFactory(LANDSLIDE_DATA_FILE_PATH, INPUT_FILE_PATH, "NASA_GLOBAL_LANDSLIDE")
    builder = factory.create_csv_builder()
    builder.build_input_csv_file()