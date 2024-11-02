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

def datetimeToString(dtAt: datetime.datetime, format = "%Y.%m.%d %H:%M:%S") -> str:
    """Convert a datetime object to string like 2023.12.28 13:15:36."""
    #return dtAt.strftime(format)
    return timestampToString(dtAt.timestamp(), format)

def timestampToDatetimeUTC(tAt: float) -> datetime.datetime:
    """Convert a float timestamp to a UTC aware datetime object."""
    return pytz.UTC.localize(datetime.datetime.utcfromtimestamp(tAt))

def stringToTimestamp(strExif: str, format = "%Y.%m.%d %H:%M:%S") -> float:
    """Convert string like 2023.12.28 13:15:36 to float timestamp."""
    return time.mktime(datetime.datetime.strptime(strExif, format).timetuple())

def exifToTimestamp(strExif: str) -> float:
    """Convert EXIF string like 2023:12:28 13:15:36 to float timestamp."""
    return stringToTimestamp(strExif, "%Y:%m:%d %H:%M:%S")

def nowAsString(format = "%Y.%m.%d %H:%M:%S") -> str:
    """Formats the current local timestamp like 2023.12.28 13:15:36."""
    return timestampToString(time.time(), format)

def now() -> float:
    """Returns the current timestamp as float."""
    return time.time()

def addDays(tAt: float, nDays: int) -> float:
    """Adds the specified number of days to the float timestamp."""
    return tAt + 24*3600*nDays

def testDateTools():
    log = logging.getLogger('DateTools')
    tNow = now()
    log.info('Now as timestamp is %f', tNow)
    log.info('Now as local str is %s', timestampToString(tNow))
    log.info('Now as UTC date  is %s', timestampToDatetimeUTC(tNow))
    log.info('Tomorrow is %s', timestampToString(addDays(tNow, 1)))

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", 
        datefmt = '%Y.%m.%d %H:%M:%S',
        level=logging.INFO, 
        handlers=[logging.StreamHandler()])
    testDateTools()