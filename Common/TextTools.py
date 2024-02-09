"""
 Helper methods for formatting text.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging

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
    return str


def testTextTools():
    log = logging.getLogger('TextTools')
    log.info('Distance is %s', distanceToString(1000.0/3.0))
    log.info('Distance is %s', distanceToString(23456.7))
    log.info('Duration is %s', durationToString(1.234))
    log.info('Duration is %s', durationToString(2*60 + 30))
    log.info('Duration is %s', durationToString(3*3600 + 15*60 + 42))

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", 
        datefmt = '%Y.%m.%d %H:%M:%S',
        level=logging.INFO, 
        handlers=[logging.StreamHandler()])
    testTextTools()