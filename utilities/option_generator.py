from utilities.option_parser import OptionParser
from constants import DOWNLOADED_BASE_PATH, METADATA_CATALOG, INPUT_FILE_PATH, BACKUP_FILE_PATH
def generate_options():
    parser = OptionParser()
    parser.add_option("-o", "--option", dest="option", action="store", type="choice",
                        help="latlng or liste or catalog or bulk_latlng", choices=['latlng', 'liste', 'catalog', 'bulk_latlng'], default=None)
    parser.add_option("-l", "--liste", dest="fic_liste", action="store", type="string",
                        help="list filename", default=None)
    parser.add_option("--input", dest="input", action="store", type="string",
                        help="input csv file", default=INPUT_FILE_PATH)
    parser.add_option("--backup", dest="backup", action="store", type="string",
                        help="backup csv file", default=BACKUP_FILE_PATH)                  
    parser.add_option("--latitude", dest="latitude", action="store", type="float",
                        help="Latitude of scene")
    parser.add_option("--longitude", dest="longitude", action="store", type="float",
                        help="Longitude of scene")
    parser.add_option("-d", "--start_date", dest="start_date", action="store", type="string",
                        help="start date, fmt('20131223')")
    parser.add_option("-f", "--end_date", dest="end_date", action="store", type="string",
                        help="end date, fmt('20131223')")
    parser.add_option("-c", "--cloudcover", dest="clouds", action="store", type="float",
                        help="Set a limit to the cloud cover of the image", default=None)
    parser.add_option("-u", "--usgs_passwd", dest="usgs", action="store", type="string",
                        help="USGS earthexplorer account and password file")
    parser.add_option("-p", "--proxy_passwd", dest="proxy", action="store", type="string",
                        help="Proxy account and password file")
    parser.add_option("-z", "--unzip", dest="unzip", action="store", type="string",
                        help="Unzip downloaded tgz file", default=None)
    parser.add_option("-b", "--sat", dest="satellite", action="store", type="choice",
                        help="Which satellite are you looking for", choices=['LT5', 'LE7', 'LC8'], default='LC8')
    parser.add_option("--output", dest="output", action="store", type="string",
                        help="Where to download files", default=DOWNLOADED_BASE_PATH)
    parser.add_option("--outputcatalogs", dest="outputcatalogs", action="store", type="string",
                        help="Where to download metadata catalog files", default=METADATA_CATALOG)
    parser.add_option("--dir", dest="dir", action="store", type="string",
                        help="Dir number where files  are stored at USGS", default=None)
    parser.add_option("--collection", dest="collection", action="store", type="int",
                        help="Landsat collection", default=1)
    parser.add_option("--station", dest="station", action="store", type="string",
                        help="Station acronym (3 letters) of the receiving station where the file is downloaded", default=None)
    parser.add_option("-k", "--updatecatalogfiles", dest="updatecatalogfiles", action="store", type="choice",
                        help="Update catalog metadata files", choices=['update', 'noupdate'], default='noupdate')

    return parser