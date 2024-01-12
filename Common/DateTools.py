"""
 Helper methods for converting strings to timestamps.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import time
import datetime

def timestampToString(tAt: float, format = "%Y.%m.%d %H:%M:%S") -> str:
    """Convert a float timestamp to string like 2023.12.28 13:15:36."""
    return time.strftime(format, time.localtime(tAt))

def stringToTimestamp(strExif: str, format = "%Y.%m.%d %H:%M:%S") -> float:
    """Convert string like 2023.12.28 13:15:36 to float timestamp."""
    return time.mktime(datetime.datetime.strptime(strExif, format).timetuple())

def exifToTimestamp(strExif: str) -> float:
    """Convert EXIF string like 2023:12:28 13:15:36 to float timestamp."""
    return stringToTimestamp(strExif, "%Y:%m:%d %H:%M:%S")