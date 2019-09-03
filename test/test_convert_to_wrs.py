from constants import WRS_SHAPE_FILE_PATH
import sys
sys.path.insert(1, '../')

from convert_to_wrs import ConvertToWRS

converter = ConvertToWRS(WRS_SHAPE_FILE_PATH)
test_converter = converter.get_wrs(37.234332396, -115.80666344)
print(test_converter)