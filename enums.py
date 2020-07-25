from enum import Enum

# Because there are many dataset, each dataset has a different field name in the
# metadata file
# This enum class is the model for mapping between user defined general name
# and the actual field name from metadata file
class METADATA_FIELD_GENERAL_NAME(Enum):
    WRS_PATH = 'WRS_PATH',
    WRS_ROW = 'WRS_ROW',
    CLOUDCOVER = 'CLOUDCOVER'
    DATE_ACQUIRED = 'DATE_ACQUIRED'

class DatasetType(Enum):
    LANDSAT8_OLI_TIRS_C1_LEVEL1 = 'LC8'
    LANDSAT7_ETM_C1_LEVEL1 = 'LE7'
    LANDSAT5_TM_C1_LEVEL1 = 'LT5'

class METADATA_FILE_INFO(Enum):
    ORIGIN = 'ORIGIN'
    REQUEST_ID = 'REQUEST_ID'
    LANDSAT_SCENE_ID = 'LANDSAT_SCENE_ID'
    LANDSAT_PRODUCT_ID = 'LANDSAT_PRODUCT_ID'
    FILE_DATE = 'FILE_DATE'
    STATION_ID = 'STATION_ID'


class ImageAttribute(Enum):
    CLOUDCOVER = 'CLOUDCOVER'
    CLOUDCOVER_LAND = 'CLOUDCOVER_LAND'
    IMAGE_QUALITY_OLI = 'IMAGE_QUALITY_OLI'
    IMAGE_QUALITY_TIRS = 'IMAGE_QUALITY_TIRS'


class PRODUCT_METADATA(Enum):
    NADIR_OFFNADIR = 'NADIR_OFFNADIR'
    DATE_ACQUIRED = 'DATE_ACQUIRED'

# class LANDSLIDE_IMPACT_SIZE(Enum):
#     CNN_FIX = (224,224)
#     VERY_SMALL = (250, 250)
#     SMALL = (350, 350)
#     MEDIUM = (450, 450)
#     LARGE = (1300, 1300)
#     VERY_LARGE = (1800, 1800)
#     EXTRA_LARGE = (2500, 2500)
#     UNKNOWN = (750, 750)

# Paper "Landslide localization in remote sensing by a convolution neural network" configuration
# Case L1 + VL1
class LANDSLIDE_IMPACT_SIZE(Enum):
    CNN_FIX = (224,224)
    LARGE = (3333, 3333)
    VERY_LARGE = (7711, 7711)
    EXTRA_LARGE = (7711, 7711) #maxima image size