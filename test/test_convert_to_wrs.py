import sys, os
currentdir = os.path.dirname(sys.path[0]) #ref: https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
sys.path[0] = currentdir

from constants import WRS_SHAPE_FILE_PATH
from convert_to_wrs import ConvertToWRS

converter = ConvertToWRS(WRS_SHAPE_FILE_PATH)
test_converter = converter.get_wrs(37.234332396, -115.80666344)
print(test_converter)