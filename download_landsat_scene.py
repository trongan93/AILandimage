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
import pandas as pd

from constants import *
from convert_to_wrs import ConvertToWRS
from utilities.option_parser import OptionParser
from utilities.option_generator import *
from utilities.option_condition_check import *
from utilities.earthexplorer_connector import *
from utilities.metadata_processor import *
from utilities.parser import *

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
            print(e)
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

def getmetadatafiles(destdir, option):
    print('Verifying catalog metadata files...')
    home = 'https://landsat.usgs.gov/landsat/metadata_service/bulk_metadata_files/'
    links = ['LANDSAT_8.csv', 'LANDSAT_ETM.csv', 'LANDSAT_ETM_SLC_OFF.csv', 'LANDSAT_TM-1980-1989.csv',
             'LANDSAT_TM-1990-1999.csv', 'LANDSAT_TM-2000-2009.csv', 'LANDSAT_TM-2010-2012.csv']
    for l in links:
        destfile = os.path.join(destdir, l)
        url = home+l
        if option == 'noupdate':
            if not os.path.exists(destfile):
                print('Downloading %s for the first time...' % (l))
                urllib.request.urlretrieve(url, destfile)
        elif option == 'update':
            urllib.request.urlretrieve(url, destfile)

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

def get_repert_and_collection(satellite, outputcatalogs, date_start):
    """
        Get repert and collection files based on specific landsat satellite
    """
    if satellite.startswith('LC8'):
        repert = ['12864']
        collection_file = os.path.join(
            outputcatalogs, 'LANDSAT_8.csv')
    if satellite.startswith('LE7'):
        repert = ['12267']
        collection_file = os.path.join(
            outputcatalogs, 'LANDSAT_ETM.csv')
    if satellite.startswith('LT5'):
        repert = ['12266']
        if 2000 <= int(date_start.year) <= 2009:
            collection_file = os.path.join(
                outputcatalogs, 'LANDSAT_TM-2000-2009.csv')
        if 2010 <= int(date_start.year) <= 2012:
            collection_file = os.path.join(
                outputcatalogs, 'LANDSAT_TM-2010-2012.csv')

    return (repert, collection_file)

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

def organize_images(is_filter_enabled, cloudcover=None):
    for root, dirs, files in os.walk(DOWNLOADED_BASE_PATH):
        for filename in files:
            if filename.endswith("_MTL.txt"):
                attribute_values = read_attributes_in_metadata(os.path.join(root, filename), ['DATE_ACQUIRED', 'TARGET_WRS_PATH', 'TARGET_WRS_ROW', 'CLOUDCOVER'])

                # Location
                location = os.path.join(IMAGE_BASE_PATH, str(attribute_values['TARGET_WRS_PATH']).zfill(3) + str(attribute_values['TARGET_WRS_ROW']).zfill(3))
                # makedir_if_path_not_exists(location)

                # Time
                location = os.path.join(location, attribute_values['DATE_ACQUIRED'])
                # makedir_if_path_not_exists(location)

                # DatasetType
                location = os.path.join(location, filename[0:filename.index('_')])
                # makedir_if_path_not_exists(location)

                # Filter
                if is_filter_enabled == True:
                    if cloudcover != None:
                        location = os.path.join(location, "CLOUDCOVER")
                    else:
                        location = os.path.join(location, "DEFAULT FILTER")
                else:
                    location = os.path.join(location, "NO FILTER")
                # makedir_if_path_not_exists(location)

                print("Moving data...")
                shutil.copytree(root, location)
                shutil.rmtree(root)
                print("...Completed moving data")

def log(location, info):
    logfile = os.path.join(location, 'log.txt')
    log = open(logfile, 'w')
    log.write('\n'+str(info))


######################################################################################
###############                       main                    ########################
######################################################################################

def main():           
    if len(sys.argv) == 1:
        prog = os.path.basename(sys.argv[0])
        print('      '+sys.argv[0]+' [options]')
        print("Examples command: ", prog, " --help")
        print("Examples command: ", prog, " -h")
        print("example (bulk_latlng): python %s -o bulk_latlng --input input.csv --backup input_backup.csv -u usgs.txt" % sys.argv[0])
        print(
            "example (latlng): python %s -o latlng -d 20190801 -f 20190826 --latitude 37.234332396 --longitude -115.80666344 -u usgs.txt" % sys.argv[0])
        print(
            "example (latlng): python %s -z unzip -b LT5 -o latlng -d 20101001 -f 20101231 --latitude 37.234332396 --longitude -115.80666344 -u usgs.txt --output /outputdir/" % sys.argv[0])
        print(
            "example (latlng): python %s -z unzip -b LT5 -o latlng -d 20101001 -f 20101231 --latitude 37.234332396 --longitude -115.80666344 -u usgs.txt --output /outputdir/ -k update --outputcatalogs /outputcatalogsdir/" % sys.argv[0])
        print(
            "example (latlng): python %s -b LE7 -o latlng -d 20151201 -f 20151231 --latitude 37.234332396 --longitude -115.80666344 -u usgs.txt --output . --dir=12267 --station SG1" % sys.argv[0])
        sys.exit(-1)
    else:
        parser = generate_options()
        (options, args) = parser.parse_args()
        parser = check_option_condition(parser, options, args)

    ### Location(pathrow)/Time(yyyymmdd (space_time))/DatasetType(LC8, LE7, LT5)/Filter(CLOUD_COVER)   
    print(options.station, options.dir)

    downloaded_path = options.output
    if not os.path.exists(downloaded_path):
        os.mkdir(downloaded_path)
        if options.option == 'liste':
            if not os.path.exists(downloaded_path+'/LISTE'):
                os.mkdir(downloaded_path+'/LISTE')

    # read password files
    try:
        f = open(options.usgs)
        (account, passwd) = f.readline().split(' ')
        if passwd.endswith('\n'):
            passwd = passwd[:-1]
        usgs = {'account': account, 'passwd': passwd}
        f.close()
    except:
        print("error with usgs password file")
        sys.exit(-2)

    if options.proxy != None:
        try:
            f = file(options.proxy)
            (user, passwd) = f.readline().split(' ')
            if passwd.endswith('\n'):
                passwd = passwd[:-1]
            host = f.readline()
            if host.endswith('\n'):
                host = host[:-1]
            port = f.readline()
            if port.endswith('\n'):
                port = port[:-1]
            proxy = {'user': user, 'pass': passwd, 'host': host, 'port': port}
            f.close()
        except:
            print("error with proxy password file")
            sys.exit(-3)

    wrs_converter = ConvertToWRS(WRS_SHAPE_FILE_PATH)

    if options.option == 'catalog':
        satellite = options.satellite
        path = options.scene[0:3]
        row = options.scene[3:6]

        date_start = parse_date(options.start_date)
        downloaded_ids = []

        if options.end_date != None:
            date_end = parse_date(options.end_date)
        else:
            date_end = datetime.datetime.now()

        if options.proxy != None:
            connect_earthexplorer_proxy(proxy, usgs)
        else:
            connect_earthexplorer_no_proxy(usgs)

        location = DOWNLOADED_BASE_PATH + '/' + str(path).zfill(3) + str(row).zfill(3)
        if not(os.path.exists(location)):
            os.makedirs(location)

        getmetadatafiles(options.outputcatalogs, options.updatecatalogfiles)

        (repert, collection_file) = get_repert_and_collection(satellite, options.outputcatalogs, date_start)       

        check = 1

        notfound = False

        product_id = find_in_collection_metadata(
            collection_file, options.clouds, date_start, date_end, path, row)
        if product_id == '':
            sys.exit(
                'No image was found in the catalog with the given specifications! Exiting...')
        else:
            tgzfile = os.path.join(location, product_id+'.tgz')
            lsdestdir = os.path.join(location, product_id)

        if os.path.exists(lsdestdir):
            print('   product %s already downloaded and unzipped' % product_id)
            downloaded_ids.append(product_id)
            check = 0
        elif os.path.isfile(tgzfile):
            print('   product %s already downloaded' % product_id)
            if options.unzip != None:
                p = unzipimage(product_id, location)
                if p == 1:
                    downloaded_ids.append(product_id)
                    check = 0
        else:
            while check == 1:
                for collectionid in repert:
                    url = "https://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE" % (
                        collectionid, product_id)
                    try:
                        downloadChunks(url, "%s" % location, product_id+'.tgz')
                    except:
                        print('   product %s not found' % product_id)
                        notfound = True
                    if notfound != True and options.unzip != None:
                        p = unzipimage(product_id, location)
                        if p == 1 and options.clouds != None:
                            check = check_cloud_limit(
                                lsdestdir, options.clouds)
                            if check == 0:
                                downloaded_ids.append(product_id)

    if options.option == 'liste':
        with open(options.fic_liste) as f:
            lignes = f.readlines()
        for ligne in lignes:
            (site, product_id) = ligne.split(' ')
            satellite = product_id.strip()
            print(satellite)
            (repert, stations) = get_repert_and_stations(satellite)

            if not os.path.exists(downloaded_path+'/'+site):
                os.mkdir(downloaded_path+'/'+site)
            url = "https://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE" % (
                repert, satellite)
            print('url=', url)
            try:
                if options.proxy != None:
                    connect_earthexplorer_proxy(proxy, usgs)
                else:
                    connect_earthexplorer_no_proxy(usgs)

                downloadChunks(url, downloaded_path+'/'+site, satellite+'.tgz')
            except TypeError:
                print('satellite %s does not exist' % satellite)

    if options.option == 'latlng':
        satellite = options.satellite
        lat = options.latitude
        lng = options.longitude

        wrs = wrs_converter.get_wrs(lat, lng)
        print(wrs)
        for cell in wrs:
            path = cell["path"]
            row = cell["row"]

            date_start = parse_date(options.start_date)
            downloaded_ids = []

            if options.end_date != None:
                date_end = parse_date(options.end_date)
            else:
                date_end = datetime.datetime.now()

            if options.proxy != None:
                connect_earthexplorer_proxy(proxy, usgs)
            else:
                connect_earthexplorer_no_proxy(usgs)


            location = DOWNLOADED_BASE_PATH

            (repert, stations) = get_repert_and_stations(satellite)

            if options.station != None:
                stations = [options.station]
            if options.dir != None:
                repert = options.dir

            check = 1

            curr_date = next_overpass(date_start, int(path), satellite)

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
                        tgzfile = os.path.join(location, product_id+'.tgz')
                        lsdestdir = os.path.join(location, product_id)
                        url = "https://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE" % (
                            repert, product_id)
                        print(url)
                        if os.path.exists(lsdestdir):
                            print('product %s already downloaded and unzipped' % product_id)
                            isFilterEnabled = options.cloud != None
                            organize_images(isFilterEnabled, options.clouds)
                            check = 0
                        elif os.path.isfile(tgzfile):
                            print('product %s already downloaded' % product_id)
                            if options.unzip != None:
                                p = unzipimage(product_id, location)
                                if p == 1 and options.clouds != None:
                                    check = check_cloud_limit(lsdestdir, options.clouds)
                                if check == 1:
                                    isFilterEnabled = options.cloud != None
                                    organize_images(isFilterEnabled, options.clouds)
                        else:
                            try:
                                downloadChunks(url, "%s" % location, product_id+'.tgz')
                            except:
                                print('   product %s not found' % product_id)
                                notfound = True
                            if notfound != True and options.unzip != None:
                                p = unzipimage(product_id, location)
                                if p == 1 and options.clouds != None:
                                    check = check_cloud_limit(lsdestdir, options.clouds)

    if options.option == 'bulk_latlng':
        inputf = options.input
        backupf = options.backup

        with open(inputf, "r") as f:
            input_csv = csv.DictReader(f, delimiter=',')

            for line in input_csv:
                lat = float(line["lat"])
                lng = float(line["lng"])
                start_date = str(line["start_date"])
                end_date = str(line["end_date"])
                unzip = bool(line["unzip"])
                satellite = line["satellite"]
                station = line["station"]
                cloudcover = line["cloudcover"]
                
                wrs = wrs_converter.get_wrs(lat, lng)
                print(wrs)
                for cell in wrs:
                    path = cell["path"]
                    row = cell["row"]

                    date_start = parse_date(start_date)
                    downloaded_ids = []

                    if end_date != None:
                        date_end = parse_date(end_date)
                    else:
                        date_end = datetime.datetime.now()

                    if options.proxy != None:
                        connect_earthexplorer_proxy(proxy, usgs)
                    else:
                        connect_earthexplorer_no_proxy(usgs)

                    location = DOWNLOADED_BASE_PATH

                    (repert, stations) = get_repert_and_stations(satellite)

                    if station != None:
                        stations = [station]

                    check = 1

                    curr_date = next_overpass(date_start, int(path), satellite)

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
                                tgzfile = os.path.join(location, product_id+'.tgz')
                                lsdestdir = os.path.join(location, product_id)
                                url = "https://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE" % (repert, product_id)
                                print(url)
                                if os.path.exists(lsdestdir):
                                    print('product %s already downloaded and unzipped' % product_id)
                                    isFilterEnabled = options.cloud != None
                                    organize_images(isFilterEnabled, options.clouds)
                                    check = 0
                                elif os.path.isfile(tgzfile):
                                    print('product %s already downloaded' % product_id)
                                    if unzip != None:
                                        p = unzipimage(product_id, location)
                                        if p == 1 and cloudcover != None:
                                            check = check_cloud_limit(lsdestdir, cloudcover)
                                        if check == 1:
                                            isFilterEnabled = options.cloud != None
                                            organize_images(isFilterEnabled, options.clouds)
                                else:
                                    try:
                                        downloadChunks(url, "%s" % location, product_id+'.tgz')
                                    except:
                                        print('product %s not found' % product_id)
                                        notfound = True
                                    if notfound != True and options.unzip != None:
                                        p = unzipimage(product_id, location)
                                        if p == 1 and options.clouds != None:
                                            check = check_cloud_limit(lsdestdir, cloudcover)
                
                with open(backupf, 'a') as backup:
                    writer = csv.writer(backup)
                    writer.writerow(line.values())
                

            




if __name__ == "__main__":
    organize_images(True, cloudcover=None)
    # main()        