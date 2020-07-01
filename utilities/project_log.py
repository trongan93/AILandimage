'''
Log file to log all the process
Created by trongan93 - June 10th 2020
'''
from constants import *
import logging
from datetime import datetime
import pytz
tz_Taipei = pytz.timezone('Asia/Taipei')


class LogProgram():

    def __init__(self,fileName):
        logging.basicConfig(filename=''.join([LOG_PATH, fileName, '.log']), filemode='w',format='%(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.info(''.join([fileName,' is started - ', datetime.now(tz_Taipei).strftime("%m/%d/%Y %H:%M:%S")]))
    def info(self,INFO_MESS):
        logger = logging.getLogger(__name__)
        logger.info(INFO_MESS)