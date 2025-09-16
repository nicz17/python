"""
 Helper methods for formatting text.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import re

def distanceToString(dist: float) -> str:
    """Convert a distance in meters to human-readable text."""
    str = f'{dist:.2f}m'
    if dist > 1000:
        str = f'{dist/1000.0:.1f}km'
    return str

def durationToString(dur: float) -> str:
    """Convert a duration in seconds to human-readable text."""
    str = f'{dur:.3f}s'
    if dur > 3600:
        hours = int(dur/3600)
        min = int((dur - 3600*hours)/60)
        str = f'{hours}h{min}m'
    elif dur > 60:
        min = int(dur/60)
        sec = int(dur - 60*min)
        str = f'{min}m{sec}s'
    elif dur > 1.0:
        str = f'{dur:.1f}s'
    return str

def upperCaseFirst(text: str) -> str:
    """Return the specified text with the first char in upper case."""
    if text is None:
        return None
    return text[:1].upper() + text[1:]

def lowerCaseFirst(text: str) -> str:
    """Return the specified text with the first char in lower case."""
    if text is None:
        return None
    return text[:1].lower() + text[1:]

def splitCamelCase(text: str) -> str:
    """Split camel-case into separate words."""
    result = str(re.sub(r"([A-Z][a-z])", r" \1", text).lower())
    return result

def replaceAccents(text: str) -> str:
    """Return a copy of the string with french accents replaced by ordinary letters."""
    if text is None: 
        return None
    result = text
    result = result.replace('à', 'a')
    result = result.replace('â', 'a')
    result = result.replace('é', 'e')
    result = result.replace('è', 'e')
    result = result.replace('ê', 'e')
    result = result.replace('ï', 'i')
    result = result.replace('î', 'i')
    result = result.replace('ô', 'o')
    return result

def removeDigits(text: str) -> str:
    """Return a copy of the string with digits removed."""
    return ''.join([ch for ch in text if not ch.isdigit()])

def fileSizeToString(size: int) -> str:
    """Formats a file size to human-readable."""
    if size > 1024**3:
        return f'{int(size/(1024**3))}GB'
    if size > 1024*1024:
        return f'{int(size/(1024*1024))}MB'
    if size > 1024:
        return f'{int(size/1024)}kB'
    return f'{size}B'

def testTextTools():
    log = logging.getLogger('TextTools')
    log.info('Distance is %s', distanceToString(1000.0/3.0))
    log.info('Distance is %s', distanceToString(23456.7))
    log.info('Duration is %s', durationToString(1.234))
    log.info('Duration is %s', durationToString(2*60 + 30))
    log.info('Duration is %s', durationToString(3*3600 + 15*60 + 42))
    log.info('upperCaseFirst: %s', upperCaseFirst('welcome to Lausanne!'))
    log.info('lowerCaseFirst: %s', lowerCaseFirst('GetTitle()'))
    log.info('splitCamelCase: %s', splitCamelCase('myCamelCaseName'))
    log.info('replaceAccents: %s', replaceAccents('Eté à âme amère'))
    log.info('removeDigits: %s', removeDigits('H3770w0r1d'))

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", 
        datefmt = '%Y.%m.%d %H:%M:%S',
        level=logging.INFO, 
        handlers=[logging.StreamHandler()])
    testTextTools()