#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
    Landsat Data download from earth explorer
"""
import os
import sys
import math
import urllib
import urllib.request
import urllib.response
import urllib.parse
import urllib.error
import time
import subprocess
import datetime
import csv
import re
import json

from constants import *
from convert_to_wrs import ConvertToWRS
from utilities.earthexplorer_connector import *
from utilities.metadata_processor import *
from utilities.parser import *
from utilities.mapper import *

def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def downloadChunks(url, rep, nom_fic):
    """ Downloads large files in pieces
     inspired by http://josh.gourneau.com
    """
    try:
        req = urllib.request.urlopen(url)
        # if downloaded file is html
        if (req.info().get_content_type() == 'text/html'):
            print("error : file is in html and not an expected binary file")
            lines = req.read()
            if lines.find('Download Not Found') > 0:
                raise TypeError
            else:
                with open("error_output.html", "w") as f:
                    f.write(lines)
                print("result saved in ./error_output.html")
                sys.exit(-1)
        # if file too small

        total_size = int(req.headers['Content-Length'].strip())
        if (total_size < 50000):
            print("Error: The file is too small to be a Landsat Image")
            print(url)
            sys.exit(-1)
        print(nom_fic, total_size)
        total_size_fmt = sizeof_fmt(total_size)

        # download
        downloaded = 0
        CHUNK = 1024 * 1024 * 8
        with open(rep+'/'+nom_fic, 'wb') as fp:
            start = time.process_time()
            print('Downloading {0} ({1}):'.format(nom_fic, total_size_fmt))
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                done = int(50 * downloaded / total_size)
                sys.stdout.write('\r[{1}{2}]{0:3.0f}% {3}ps'
                                 .format(math.floor((float(downloaded)
                                                     / total_size) * 100),
                                         '=' * done,
                                         ' ' * (50 - done),
                                         sizeof_fmt((downloaded // (time.process_time() - start)) / 8)))
                sys.stdout.flush()
                if not chunk:
                    break
                fp.write(chunk)
    except urllib.error.HTTPError as e:
        if e.code == 500:
            # print(e)
            pass  # File doesn't exist
        else:
            print("HTTP Error:", e.code, url)
        return False
    except urllib.error.URLError as e:
        print("URL Error:", e.reason, url)
        return False

    return rep, nom_fic

def cycle_day(path):
    """ provides the day in cycle given the path number
    """
    cycle_day_path1 = 5
    cycle_day_increment = 7
    nb_days_after_day1 = cycle_day_path1+cycle_day_increment*(path-1)

    cycle_day_path = math.fmod(nb_days_after_day1, 16)
    if path >= 98:  # change date line
        cycle_day_path += 1
    return(cycle_day_path)

def next_overpass(date1, path, sat):
    """ provides the next overpass for path after date1
    """
    date0_L5 = datetime.datetime(1985, 5, 4)
    date0_L7 = datetime.datetime(1999, 1, 11)
    date0_L8 = datetime.datetime(2013, 5, 1)

    if sat == 'LT5':
        date0 = date0_L5
    elif sat == 'LE7':
        date0 = date0_L7
    elif sat == 'LC8':
        date0 = date0_L8
    next_day = math.fmod((date1-date0).days-cycle_day(path)+1, 16)
    if next_day != 0:
        date_overpass = date1+datetime.timedelta(16-next_day)
    else:
        date_overpass = date1
    return(date_overpass)

def unzipimage(tgzfile, outputdir):
    """
    Unzip tgz file
    """
    success = 0
    if (os.path.exists(outputdir+'/'+tgzfile+'.tgz')):
        print("\nunzipping...")
        try:
            if sys.platform.startswith('linux'):
                subprocess.call('mkdir ' + outputdir+'/' +
                                tgzfile, shell=True)  # Unix
                subprocess.call('tar zxvf '+outputdir+'/'+tgzfile +
                                '.tgz -C ' + outputdir+'/'+tgzfile, shell=True)  # Unix
            elif sys.platform.startswith('win'):
                subprocess.call('tartool '+outputdir+'/'+tgzfile +
                                '.tgz ' + outputdir+'/'+tgzfile, shell=True)  # W32
            success = 1
        except TypeError:
            print('Failed to unzip %s' % tgzfile)
        os.remove(outputdir+'/'+tgzfile+'.tgz')
    return success

def get_repert_and_stations(satellite):
    """
        Get repert andd stations based on specific landsat satellite
    """
    if satellite.startswith('LC8'):
        repert = '12864'
        stations = ['LGN']
    if satellite.startswith('LE7'):
        repert = '12267'
        stations = ['EDC', 'SGS', 'AGS', 'ASN', 'SG1']
    if satellite.startswith('LT5'):
        repert = '12266'
        stations = ['ASN', 'GLC', 'ASA', 'KIR', 'MOR', 'KHC',
                    'PAC', 'KIS', 'CHM', 'LGS', 'MGR', 'COA', 'MPS', 'JSA']
    return (repert, stations)

def makedir_if_path_not_exists(path):
    if not(os.path.exists(path)):
        os.mkdir(path)

def get_valid_metadata_field_names_based_on_satellite(satellite):
    attribute_names = ['DATE_ACQUIRED']
    if satellite == 'LE07':
        attribute_names.extend(['WRS_PATH', 'WRS_ROW', 'CLOUD_COVER'])
    elif satellite == 'LC08':
        attribute_names.extend(['WRS_PATH', 'WRS_ROW', 'CLOUD_COVER'])
    elif satellite == 'LT05':
        attribute_names.extend(['WRS_PATH', 'WRS_ROW', 'CLOUD_COVER'])

    return attribute_names

def get_general_field_name_from_mapper(mapper, satellite, general_name):
    return mapper[(satellite, general_name)]

def move_images_after_downloaded(lsdestdir, is_filter_enabled, cloudcover=None):
    mapper = map_metadata_fieldname_to_general_name()

    for root, dirs, files in os.walk(lsdestdir):
        for filename in files:
            if filename.endswith("_MTL.txt"):
                cloudcover_percent = read_cloudcover_in_metadata(filename)

                satellite = parse_satellite_from_downloaded_filename(filename)
                attribute_names = get_valid_metadata_field_names_based_on_satellite(satellite)

                attribute_values = read_attributes_in_metadata(os.path.join(root, filename), attribute_names)

                path = str(attribute_values[get_general_field_name_from_mapper(mapper, satellite, 'WRS_PATH')]).zfill(3)
                row = str(attribute_values[get_general_field_name_from_mapper(mapper, satellite, 'WRS_ROW')]).zfill(3)
                # Location
                location = os.path.join(IMAGE_BASE_PATH, path + row)
                makedir_if_path_not_exists(location)

                # Time
                location = os.path.join(location, attribute_values['DATE_ACQUIRED'])
                makedir_if_path_not_exists(location)

                # DatasetType
                location = os.path.join(location, parse_satellite_from_downloaded_filename(filename))
                makedir_if_path_not_exists(location)

                # Filter (CLOUDCOVER_PERCENT)
                filter_folder_name = f"{str(int(cloudcover_percent))}"
                location = os.path.join(location, filter_folder_name)
                makedir_if_path_not_exists(location)

                print("Moving data...")
                for copiedFiles in files:
                    shutil.copy2(os.path.join(root, copiedFiles), location)
                shutil.rmtree(root)
                os.mkdir(root)
                print("...Completed moving data")

                return location

def organize_images(is_filter_enabled, cloudcover=None):
    mapper = map_metadata_fieldname_to_general_name()
    downloaded_path = ""

    for root, dirs, files in os.walk(os.path.join(DOWNLOADED_BASE_PATH, 'tmp')):
        for filename in files:
            if filename.endswith("_MTL.txt"):
                satellite = parse_satellite_from_downloaded_filename(filename)
                attribute_names = get_valid_metadata_field_names_based_on_satellite(satellite)

                attribute_values = read_attributes_in_metadata(os.path.join(root, filename), attribute_names)

                path = str(attribute_values[get_general_field_name_from_mapper(mapper, satellite, 'WRS_PATH')]).zfill(3)
                row = str(attribute_values[get_general_field_name_from_mapper(mapper, satellite, 'WRS_ROW')]).zfill(3)
                # Location
                location = os.path.join(IMAGE_BASE_PATH, path + row)
                makedir_if_path_not_exists(location)

                # Time
                location = os.path.join(location, attribute_values['DATE_ACQUIRED'])
                makedir_if_path_not_exists(location)

                # DatasetType
                location = os.path.join(location, parse_satellite_from_downloaded_filename(filename))
                makedir_if_path_not_exists(location)

                # Filter
                if is_filter_enabled == True:
                    if cloudcover != None:
                        location = os.path.join(location, "CLOUDCOVER")
                    else:
                        location = os.path.join(location, "DEFAULT_FILTER")
                else:
                    location = os.path.join(location, "NO_FILTER")
                makedir_if_path_not_exists(location)

                print("Moving data...")
                for copiedFiles in files:
                    shutil.copy2(os.path.join(root, copiedFiles), location)
                shutil.rmtree(root)
                os.mkdir(root)
                print("...Completed moving data")

def log(location, info):
    logfile = os.path.join(location, 'log.txt')
    log = open(logfile, 'w')
    log.write('\n'+str(info))

def read_usgs_credential_file():
    usgs = {'account': 'Me', 'passwd': 'Secret'}
    try:
        f = open(USGS_CREDENTIAL_FILE)
        (account, passwd) = f.readline().split(' ')
        if passwd.endswith('\n'):
            passwd = passwd[:-1]
        usgs = {'account': account, 'passwd': passwd}
        f.close()
    except:
        print("error with usgs password file")
        sys.exit(-2)
    return usgs

######################################################################################
###############                       main                    ########################
######################################################################################

def download_scene(input_file, csv_data):
    """ Download landsat scene with data from csv file
    
    Parameter:
    input_file (string): The CSV file
    csv_data (dict): Data from CSV file

    Returns:
    0 if the scenes are already downloaded
    downloaded_paths (string) if the scenes are downloaded and stored 
    (The downloaded_paths delimeter is a semicolon (;) )
    """           

    usgs = read_usgs_credential_file()
    wrs_converter = ConvertToWRS(WRS_SHAPE_FILE_PATH)
    
    id = csv_data["id"]
    lat = float(csv_data["lat"])
    lng = float(csv_data["lng"])
    start_date = str(csv_data["start_date"])
    end_date = str(csv_data["end_date"])
    satellite = csv_data["satellite"]
    station = csv_data["station"]
    cloudcover = csv_data["cloudcover"]
    size = csv_data["size"]
    downloaded_path = csv_data["downloaded_path"]
    
    print(id, lat, lng, start_date, end_date, size, satellite, station, cloudcover, downloaded_path)
    if downloaded_path != None and downloaded_path != "":
        print("Images already downloaded. Here is the path to image's folder")
        paths = downloaded_path.split(';')
        for path in paths:
            print(path)
        # print(path for path in paths)
        return 0

    wrs = wrs_converter.get_wrs(lat, lng)
    print(wrs)
    for cell in wrs:
        path = cell["path"]
        row = cell["row"]

        date_start = parse_date(start_date)

        if end_date != None:
            date_end = parse_date(end_date)
        else:
            date_end = datetime.datetime.now()

        connect_earthexplorer_no_proxy(usgs)

        location = os.path.join(DOWNLOADED_BASE_PATH, 'tmp')
        data_folder = os.path.join(DOWNLOADED_BASE_PATH, 'Images')     
        makedir_if_path_not_exists(location)
        makedir_if_path_not_exists(data_folder)

        (repert, stations) = get_repert_and_stations(satellite)

        if station != None and station != 'ALL':
            stations = [station]

        check = 1
        
        curr_date = next_overpass(date_start, int(path), satellite)
        image_locations = ""
        while (curr_date < date_end) and check == 1:
            date_asc = curr_date.strftime("%Y%j")
            notfound = False
            print('Searching for images on (julian date): ' + date_asc + '...')
            curr_date = curr_date+datetime.timedelta(16)
            for station in stations:
                for version in ['00', '01', '02']:
                    product_id = satellite + \
                        str(path).zfill(3)+str(row).zfill(3) + \
                        date_asc+station+version
                    
                    tgzfile = os.path.join(location, product_id + '.tgz')
                    lsdestdir = os.path.join(location, product_id)
                    print(lsdestdir)
                    if (os.path.exists(lsdestdir)):
                        print("product already downloaded and unzipped.")
                        break
                    elif (os.path.exists(tgzfile)):
                        print("product already downloaded")

                    url = "https://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE" % (repert, product_id)
                    print(url)

                    try:
                        downloadChunks(url, "%s" % location, product_id+'.tgz')
                    except:
                        print('product %s not found' % product_id)
                        notfound = True

                    if notfound != True:
                        p = unzipimage(product_id, location)
                        if p == 1 and cloudcover != None and cloudcover != "":
                            check = check_cloud_limit(lsdestdir, float(cloudcover))
                        if check == 1:
                            isFilterEnabled = cloudcover != None

                            image_location = move_images_after_downloaded(lsdestdir, isFilterEnabled, cloudcover)
                            if image_location != None:
                                image_locations += '%s;' % image_location
                            # organize_images(isFilterEnabled, cloudcover)
    
    return image_locations

