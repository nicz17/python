"""
 A simple timing class.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import time


class Timer:
    """A simple timing class."""

    def __init__(self) -> None:
        """Constructor, also starts the timer."""
        self.tStart = time.time()
        self.tEnd = None

    def start(self):
        """Starts or restarts the timer."""
        self.tStart = time.time()

    def stop(self):
        """Stops the timer."""
        self.tEnd = time.time()

    def getElapsedSeconds(self):
        """Returns the elapsed time in seconds as a float."""
        tUntil = self.tEnd if self.tEnd else time.time()
        return tUntil - self.tStart

    def getElapsed(self) -> str:
        """Returns the elapsed time as a string, formatted with millisecond precision."""
        tUntil = self.tEnd if self.tEnd else time.time()
        return f'{(tUntil - self.tStart):.3}s'
        #return '%.3fs' % (self.tEnd - self.tStart)

class TimedTask:
    """A task with a timer for performance."""
    log = logging.getLogger('TimedTask')

    def __init__(self, desc: str):
        self.timer = Timer()
        self.desc = desc
        self.log.info(f'Starting task {desc}')

    def done(self):
        """Log that task is done, with timing."""
        self.log.info(f'Done {self.desc} in {self.timer.getElapsed()}')

    def __str__(self):
        return f'TimedTask {self.desc}'