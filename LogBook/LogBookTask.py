"""
A task with steps for the LogBook app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import time

class LogBookTask:
    """A task with steps for the LogBook app."""
    log = logging.getLogger(__name__)

    def __init__(self, title, steps = []):
        self.title = title
        self.steps = steps

    def toJson(self):
        """Export this task as JSON."""
        data = {
            'title': self.title,
            #'created': DateTools.timestampToString(self.created),
            'steps': self.steps
        }
        return data
    
    @staticmethod
    def fromJson(data):
        """Load data from a JSON object."""
        title = data.get('title')
        #self.created = DateTools.stringToTimestamp(data.get('created'))
        steps = data.get('steps')
        return LogBookTask(title, steps)