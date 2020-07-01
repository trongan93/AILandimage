DOWNLOADED_BASE_PATH = '/mnt/d/ProjectData/Landsat'
IMAGE_BASE_PATH = '/mnt/d/ProjectData/Landsat/Images'
INPUT_FILE_PATH = 'input_test_June8_2020.csv'
LANDSLIDE_DATA_FILE_PATH = 'landslidedata.csv'
WRS_SHAPE_FILE_PATH = 'wrs2_shapefiles/wrs2_descending.shp'
USGS_CREDENTIAL_FILE = 'usgs.txt'
LOG_PATH = '/mnt/d/ProjectData/Logs/'

DATASET_TYPE = ['LC8', 'LE7', 'LT5']
FILTER = ['CLOUDCOVER']

RANDOM_DISTANCE_FROM_LANDSLIDE_POINT = [20, 40, 80, 160] # kilometter
RANDOM_DISTANCE_BEARING_FROM_LANDSLIDE_POINT = [0, 90, 180, 270] #0-360 degree