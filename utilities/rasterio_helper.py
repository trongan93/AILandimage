# ref https://geohackweek.github.io/raster/04-workingwithrasters/
# Image Coordinates (row, col) correspond to the row and column for a specific pixel
# Spatial Coordinates (east, north) correspond to the location of each pixel on the surface of the Earth. 

import rasterio
import rasterio.plot
import pyproj
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import time
import pickle

DEFAULT_CRS = 'epsg:32611'
DEFAULT_UTM_PROJECT_SYSTEM = 'epsg:4326'

lnglat = pyproj.Proj(init=DEFAULT_UTM_PROJECT_SYSTEM)

def lnglat_to_spatial_coors(lng, lat, crs=DEFAULT_CRS):
    utm = pyproj.Proj(crs)
    east, north = pyproj.transform(lnglat, utm, lng, lat)
    return (east, north)

def lnglat_to_image_coors(path, lng, lat):
    with rasterio.open(path) as src:
        # print(lng)
        # print(lat)
        east, north = lnglat_to_spatial_coors(lng, lat, src.crs)
        row, col = src.index(east, north)

        return (row, col)

def image_coors_to_spatial_coors(path, row, col):
    with rasterio.open(path) as src:
        east, north = src.xy(row, col)

    return (east, north)

def image_coors_to_lnglat(path, row, col):
    with rasterio.open(path) as src:
        utm = pyproj.Proj(src.crs)    
    
        # image coors (row, col) --> spatial coordinates
        east, north = src.xy(row,col) 
        # spatial coordinates --> lng, lat
        lng,lat = pyproj.transform(utm, lnglat, east, north)

    return (lng, lat)   
