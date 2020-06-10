import pandas as pd
import geopy
from geopy.distance import VincentyDistance
from constants import RANDOM_DISTANCE_FROM_LANDSLIDE_POINT as random_distances
from constants import RANDOM_DISTANCE_BEARING_FROM_LANDSLIDE_POINT as random_bearings

def create_negative_landslide(inputf):
    # ref: https://stackoverflow.com/questions/4530943/calculating-a-gps-coordinate-given-a-point-bearing-and-distance/4531227#4531227
    print('filename: ', inputf)
    data1 = pd.read_csv(inputf)
    # print('keys: ', data1.keys())

    for index, row in data1.iterrows():
        landslide_point = geopy.Point(row['lat'],row['lng'])
        random_withoutlandslide_points = []
        # print('origin lat: ', landslide_point.latitude, ' , origin lng: ', landslide_point.longitude)
        for random_dist in random_distances:
            for random_bearing in random_bearings:
                new_point = VincentyDistance(kilometers=random_dist).destination(landslide_point,random_bearing)
                random_withoutlandslide_points.append(new_point)
                # print('new point lat: ', new_point.latitude, ' , origin lng: ', new_point.longitude)
        # print('size of random points is ', len(random_withoutlandslide_points))
        # download_path = row['']



    print("Done create negative landslide data")