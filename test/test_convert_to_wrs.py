import sys
sys.path.insert(1, '../')

from convert_to_wrs import ConvertToWRS

converter = ConvertToWRS("./wrs2_shapefiles/wrs2_descending.shp")
test_converter = converter.get_wrs(37.234332396, -115.80666344)
print(test_converter)