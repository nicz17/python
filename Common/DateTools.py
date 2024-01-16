"""
 Helper methods for converting strings to timestamps.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import time
import datetime
import logging
import pytz

def timestampToString(tAt: float, format = "%Y.%m.%d %H:%M:%S") -> str:
    """Convert a float timestamp to string like 2023.12.28 13:15:36."""
    return time.strftime(format, time.localtime(tAt))

def timestampToDatetimeUTC(tAt: float) -> datetime.datetime:
    """Convert a float timestamp to a UTC aware datetime object."""
    return pytz.UTC.localize(datetime.datetime.utcfromtimestamp(tAt))

def stringToTimestamp(strExif: str, format = "%Y.%m.%d %H:%M:%S") -> float:
    """Convert string like 2023.12.28 13:15:36 to float timestamp."""
    return time.mktime(datetime.datetime.strptime(strExif, format).timetuple())

def exifToTimestamp(strExif: str) -> float:
    """Convert EXIF string like 2023:12:28 13:15:36 to float timestamp."""
    return stringToTimestamp(strExif, "%Y:%m:%d %H:%M:%S")


def testDateTools():
    log = logging.getLogger('DateTools')
    tNow = time.time()
    log.info('Now as timestamp is %f', tNow)
    log.info('Now as local str is %s', timestampToString(tNow))
    log.info('Now as UTC datet is %s', timestampToDatetimeUTC(tNow))

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", 
        datefmt = '%Y.%m.%d %H:%M:%S',
        level=logging.INFO, 
        handlers=[logging.StreamHandler()])
    testDateTools()