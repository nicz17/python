"""
A task with steps for the LogBook app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import time
import DateTools

class LogBookTask:
    """A task with steps for the LogBook app."""
    log = logging.getLogger(__name__)

    def __init__(self, title, steps = [], created = None):
        """Constructor with title, steps, created timestamp."""
        self.title = title
        if created is None:
            created = time.time()
        self.created = created
        self.steps = steps

    def toJson(self):
        """Export this task as JSON."""
        data = {
            'title': self.title,
            'created': DateTools.timestampToString(self.created),
            'steps': self.steps
        }
        return data
    
    @staticmethod
    def fromJson(data):
        """Load data from a JSON object."""
        title = data.get('title')
        created = DateTools.stringToTimestamp(data.get('created'))
        steps = data.get('steps')
        return LogBookTask(title, steps, created)
    
    def __str__(self):
        str = f'LogBookTask {self.title}'
        return str