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

aMonthFr = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 
            'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
formatDef = "%Y.%m.%d %H:%M:%S"

def timestampToString(tAt: float, format=formatDef) -> str:
    """Convert a float timestamp to string like 2023.12.28 13:15:36."""
    return time.strftime(format, time.localtime(tAt))

def datetimeToString(dtAt: datetime.datetime, format=formatDef) -> str:
    """Convert a datetime to localtime string like 2023.12.28 13:15:36."""
    return timestampToString(dtAt.timestamp(), format)

def datetimeToStringUTC(dtAt: datetime.datetime, format=formatDef) -> str:
    """Convert a datetime to UTC string like 2023.12.28 12:15:36."""
    return dtAt.strftime(format)

def datetimeToPrettyStringFr(dtAt: datetime.datetime) -> str:
    """Print the datetime as day month year in French."""
    sDay = '1er' if dtAt.day == 1 else str(dtAt.day)
    result = f'{sDay} {aMonthFr[dtAt.month-1]} {dtAt.year}'
    return result

def timestampToDatetimeUTC(tAt: float) -> datetime.datetime:
    """Convert a float timestamp to a UTC aware datetime object."""
    return pytz.UTC.localize(datetime.datetime.utcfromtimestamp(tAt))

def datetimeToLocal(dtAt: datetime.datetime) -> datetime.datetime:
    """Convert datetime to localtime offset-naive datetime."""
    return dtAt.astimezone(tz=None).replace(tzinfo=None)

def stringToTimestamp(strAt: str, format=formatDef) -> float:
    """Convert string like 2023.12.28 13:15:36 to float timestamp."""
    return time.mktime(datetime.datetime.strptime(strAt, format).timetuple())

def stringToDatetime(strAt: str, format=formatDef) -> datetime.datetime:
    """Convert string like 2023.12.28 13:15:36 to datetime."""
    return datetime.datetime.strptime(strAt, format)

def exifToTimestamp(strAt: str) -> float:
    """Convert EXIF string like 2023:12:28 13:15:36 to float timestamp."""
    return stringToTimestamp(strAt, "%Y:%m:%d %H:%M:%S")

def nowAsString(format=formatDef) -> str:
    """Formats the current local timestamp like 2023.12.28 13:15:36."""
    return timestampToString(time.time(), format)

def now() -> float:
    """Returns the current timestamp as float."""
    return time.time()

def nowDatetime() -> datetime.datetime:
    """Returns the current timestamp as datetime."""
    return datetime.datetime.now()

def addDays(tAt: float, nDays: int) -> float:
    """Adds the specified number of days to the float timestamp."""
    return tAt + 24*3600*nDays

def getDaysSince(dtAt: datetime.datetime) -> int:
    """Returns the number of days between dtAt and now."""
    dtNow = nowDatetime()
    diff = dtNow - dtAt
    return diff.days

def datetimeToMidnight(dt: datetime.datetime) -> datetime.datetime:
    """Truncate the specified datetime to midnight."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def validateDateString(strAt: str, format=formatDef) -> bool:
    """Validate the input string against the date format."""
    strNow = nowAsString(format)
    if not len(strNow) == len(strAt):
        return False
    try:
        datetime.datetime.strptime(strAt, format)
    except ValueError:
        return False
    return True

def timeUntilNextDSTSwitch():
    """Returns the duration in days until the next DST switch in CH."""
    tz = pytz.timezone('Europe/Zurich')
    now = datetime.datetime.now(tz)

    # Get the list of DST transition times for the current year and next year
    transitions = []
    year = now.year
    for y in (year, year + 1):
        # Get DST transition info for the year
        for dt in (datetime.datetime(y, 1, 1), datetime.datetime(y, 12, 31)):
            # Localize to timezone
            localized_dt = tz.localize(dt, is_dst=None)
            try:
                # transitions are stored in _utc_transition_times in pytz
                for trans_time in tz._utc_transition_times:
                    if trans_time.year == y and trans_time > now.replace(tzinfo=None):
                        transitions.append(tz.localize(trans_time))
            except AttributeError:
                # Some timezones may not have _utc_transition_times
                pass

    # Filter transitions that are in the future relative to now
    future_transitions = [t for t in transitions if t > now]

    if not future_transitions:
        return None  # No upcoming DST transitions found

    next_transition = min(future_transitions)
    delta = next_transition - now
    return delta.days


class TestDateTools:
    """Unit test class for DateTools."""
    log = logging.getLogger('TestDateTools')

    def run(self):
        tStart  = now()
        tNow    = now()
        dtNow   = datetime.datetime.now()
        dtFirst = datetime.datetime(2024, 8, 1, 12, 00)
        dtMay4  = datetime.datetime(2024, 5, 4, 12, 00)

        # Conversion and formatting
        self.log.info('Now as timestamp is %f', tNow)
        self.log.info('Now as local str is %s', timestampToString(tNow))
        self.log.info('Now as UTC date  is %s', timestampToDatetimeUTC(tNow))
        self.log.info('Tomorrow addDays is %s', timestampToString(addDays(tNow, 1)))
        self.log.info('Now dt in French is %s', datetimeToPrettyStringFr(dtNow))
        self.log.info('Aug 1  in French is %s', datetimeToPrettyStringFr(dtFirst))
        self.log.info('May 4  in French is %s', datetimeToPrettyStringFr(dtMay4))
        self.log.info('Today midnight   is %s', datetimeToMidnight(dtNow))

        # Validation
        self.testDateValidation('2026.09.29 20:00:00')
        self.testDateValidation('2026.se.29 20:00:00')
        self.testDateValidation('2026.15.29 20:00:00')
        self.testDateValidation('2026.09.29 20:00   ')
        self.testDateValidation('2026.09.13 14:27:5')

        # DST switch
        timeUntilSwitch = timeUntilNextDSTSwitch()
        if timeUntilSwitch:
            self.log.info(f"Time until next DST change: {timeUntilSwitch} days")
        else:
            self.log.info("No upcoming DST change found.")

        # Timing
        elapsed = now() - tStart
        self.log.info(f'Done in {elapsed:0.4f}s.')

    def testDateValidation(self, strAt: str):
        valid = validateDateString(strAt)
        result = 'invalid'
        if valid:
            at = stringToDatetime(strAt)
            result = f'valid ({at})'
        self.log.info(f'Validation: [{strAt}] is {result}')

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", 
        datefmt = '%Y.%m.%d %H:%M:%S',
        level=logging.INFO, 
        handlers=[logging.StreamHandler()])
    TestDateTools().run()