# AILandimage
AI Research on Landsat and Aerial Image

## Prerequisites
###  Install GDAL
Add new PPA
> sudo add-apt-repository ppa:ubuntugis/ppa

> sudo apt-get update

Install gdal-bin and libgdal-dev
> sudo apt-get install gdal-bin

> sudo apt-get install libgdal-dev

> export CPLUS_INCLUDE_PATH=/usr/include/gdal
> export C_INCLUDE_PATH=/usr/include/gdal

Check ORG and GDAL version
> ogrinfo --version

> gdal-config --version

Install GDAL with the correct version
> pip install GDAL=={enter gdal version here}

### Install Shapely library

> pip install shapely

## Project Setup

- Modify USGS username, password in usgs.txt file

- Modify location's input data file, WRS2 shape file location, downloaded image folder (DOWNLOADED_BASE_PATH), stored image folder (IMAGE_BASE_PATH) in constants.py file

- Add location's data to input.csv file

- The input.csv file has the following columns:
lat,lng,start_date (yyyymmdd),end_date (yyyymmdd),cloudcover,satellite,station,downloaded_path

| Column     | Type                | Value                                    |
| ------     | ----                | -----                                    |
| lat/lng    | double              |                                          |
| start_date | datetime (yyyymmdd) |                                          |
| cloudcover | boolean             | True/False                               |
| satellite  | string              | LC8/LE7/LT5                              |
| station    | string              | ALL (all stations)/LGN/EDC/... Ref (1)   |
| downloaded_path | string         | leave this field blank if the row's image has not been downloaded, otherwise the value from this field will be a concatenated string separated by semicolon (;) |

- To download satellite images based on location's data inputted to input.csv earlier, Run
> python main.py 1

- Cropped and combine images by running
> python main.py 2

After downloading an image at DOWNLOADED_BASE_PATH folder, the image will be moved to IMAGE_BASE_PATH folder with the following structure:
/location/date/satellite/filter

and the downloaded_path column in the input.csv file is appended with a new path to the new image's folder. All paths will be concatenated to a string separated by a semicolon (;)
Example: /home/test1/data/downloaded_files/Images/040034/2019-08-27/LC08/CLOUDCOVER;/home/test1/data/downloaded_files/Images/040034/2019-08-28/LC08/CLOUDCOVER

To redownload the LANDSAT data:
1. Remove the value from downloaded_path column in input.csv file
2. Remove the sub-folders, files corresponded to the row to redownload in input.csv file. The sub-folders are located in a folder defined by DOWNLOADED_BASE_PATH variable in constants.py file

(1) Each satellite (LC8, LT7, LE5) has their supported stations given in this table below:

| Satellite     | Stations                                                             |
| ----------    | --------------------                                                 |
| LC8           | LGN                                                                  |
| LT7           | EDC, SGS, AGS, ASN, SG1                                              |
| LE5           | ASN, GLC, ASA, KIR, MOR, KHC, PAC, KIS, CHM, LGS, MGR, COA, MPS, JSA |