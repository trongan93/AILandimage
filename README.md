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

Modify USGS username, password in usgs.txt file

Modify downloaded data, WRS2 shape file location in constants.py file