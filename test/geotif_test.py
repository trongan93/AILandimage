# ref: https://gis.stackexchange.com/questions/221292/retrieve-pixel-value-with-geographic-coordinate-as-input-with-gdal/221430
from osgeo import gdal

driver = gdal.GetDriverByName('GTiff')
filename = "/mnt/2A967D2D967CFB21/ProjectData/CubeSAT/USGSData/LT05_L1TP_019050_20100204_20161017_01_T1/LT05_L1TP_019050_20100204_20161017_01_T1_B7.TIF" #path to raster
dataset = gdal.Open(filename)
band = dataset.GetRasterBand(1)

cols = dataset.RasterXSize
rows = dataset.RasterYSize

transform = dataset.GetGeoTransform()

xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = -transform[5]

data = band.ReadAsArray(0, 0, cols, rows)

# (14.750000, -88.915000): From lat and long 
# UTM: 293852.32 East; 1631552.54 North
# Ref: https://www.latlong.net/lat-long-utm.html
# points_list = [(293852.32, 1631552.54),(0, 0)] #list of X,Y coordinates
points_list = [(293852.32, 1631552.54)]

for point in points_list:
    col = int((point[0] - xOrigin) / pixelWidth)
    row = int((yOrigin - point[1] ) / pixelHeight)

    print (row,col, data[row][col])
