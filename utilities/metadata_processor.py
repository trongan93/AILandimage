import os
import shutil
import csv
import datetime
# "Read image metadata

def read_attributes_in_metadata(metadatafile, attribute_names):
    """
    Read attributes from metadata file
    """
    attribute_values = dict()
    with open(metadatafile, 'r') as metadata:
        for line in metadata:
            line = line.replace('\r', '')
            for name in attribute_names:
                if line.find(name) >= 0:
                    lineval = line[line.find('= ')+2:]
                    lineval = lineval.replace('\n', '')
                    attribute_values[name] = (lineval)

    return attribute_values

def read_cloudcover_in_metadata(image_path):
    fields = ['CLOUD_COVER']
    cloud_cover = 0

    print(image_path)
    for filename in os.listdir(image_path):
        if filename.endswith('_MTL.txt'):
            metadatafile = os.path.join(image_path, filename)
            print(metadatafile)
            with open(metadatafile, 'r') as metadata:
                # metadata.replace('\r','')
                for line in metadata:
                    line = line.replace('\r', '')
                    for f in fields:
                        if line.find(f) >= 0:
                            lineval = line[line.find('= ')+2:]
                            cloud_cover = lineval.replace('\n', '')
    
    return float(cloud_cover)

# "Check cloud cover limit

def check_cloud_limit(imagepath, limit):
    removed = 0
    cloudcover = read_cloudcover_in_metadata(imagepath)
    print(cloudcover)
    if cloudcover > limit:
        shutil.rmtree(imagepath)
        print("Image was removed because the cloud cover value of " +
              str(cloudcover) + " exceeded the limit defined by the user!")
        removed = 1
    return removed
