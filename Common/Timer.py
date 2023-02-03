"""
 A simple timing class.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

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

    def getElapsed(self):
        """Returns the elapsed time as a string, formatted with millisecond precision."""
        if not self.tEnd:
            self.tEnd = time.time()
        return '%.3fs' % (self.tEnd - self.tStart)