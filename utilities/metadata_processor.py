import os
import shutil
import csv
import datetime
# "Read image metadata

def read_cloudcover_in_metadata(image_path):
    fields = ['CLOUD_COVER']
    cloud_cover = 0
    imagename = os.path.basename(os.path.normpath(image_path))
    metadatafile = os.path.join(image_path, imagename+'_MTL.txt')
    metadata = open(metadatafile, 'r')
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
    if cloudcover > limit:
        shutil.rmtree(imagepath)
        print("Image was removed because the cloud cover value of " +
              str(cloudcover) + " exceeded the limit defined by the user!")
        removed = 1
    return removed

# "Find image with desired specs in usgs entire collection metadata

def find_in_collection_metadata(collection_file, cc_limit, date_start, date_end, wr2path, wr2row):
    print("Searching for images in catalog...")
    cloudcoverlist = []
    cc_values = []
    with open(collection_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            year_acq = int(row['acquisitionDate'][0:4])
            month_acq = int(row['acquisitionDate'][5:7])
            day_acq = int(row['acquisitionDate'][8:10])
            acqdate = datetime.datetime(year_acq, month_acq, day_acq)
            if int(row['path']) == int(wr2path) and int(row['row']) == int(wr2row) and row['DATA_TYPE_L1'] != 'PR' and float(row['cloudCoverFull']) <= cc_limit and date_start < acqdate < date_end:
                cloudcoverlist.append(
                    row['cloudCoverFull'] + '--' + row['sceneID'])
                cc_values.append(float(row['cloudCoverFull']))
            else:
                sceneID = ''
    for i in cloudcoverlist:
        if float(i.split('--')[0]) == min(cc_values):
            sceneID = i.split('--')[1]
    return sceneID
