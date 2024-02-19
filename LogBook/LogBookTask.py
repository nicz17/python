"""
A task with steps for the LogBook app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import time
import DateTools
from enum import Enum

class Status(Enum):
    """Enumeration of step status."""
    Idle = 0
    Done = 1
    Cancelled = 2

    def __str__(self):
        return self.name
    
class LogBookStep:
    """A step in a LogBook task."""
    log = logging.getLogger(__name__)

    def __init__(self, text: str, status = None):
        """Constructor with text, status."""
        self.text = text
        if status is None:
            status = Status.Idle
        self.status = status

    def toJson(self):
        """Export this step as JSON."""
        data = {
            'text': self.text,
            'status': self.status.name
        }
        return data
    
    @staticmethod
    def fromJson(data):
        """Load data from a JSON object."""
        text = data.get('text')
        status = Status[data.get('status')]
        return LogBookStep(text, status)
    
    def __str__(self):
        str = f'LogBookStep {self.text} {self.status}'
        return str


class LogBookTask:
    """A task with steps for the LogBook app."""
    log = logging.getLogger(__name__)

    def __init__(self, title, steps = None, created = None):
        """Constructor with title, steps, created timestamp."""
        self.title = title
        if created is None:
            created = time.time()
        self.created = created
        if steps is None:
            steps = []
        self.steps = steps

    def addStep(self, step: LogBookStep):
        """Add a step to this task."""
        if step is not None:
            self.steps.append(step)

    def toJson(self):
        """Export this task as JSON."""
        dataSteps = []
        for step in self.steps:
            dataSteps.append(step.toJson())
        data = {
            'title': self.title,
            'created': DateTools.timestampToString(self.created),
            'steps': dataSteps
        }
        return data
    
    @staticmethod
    def fromJson(data):
        """Load data from a JSON object."""
        title = data.get('title')
        created = DateTools.stringToTimestamp(data.get('created'))
        #steps = data.get('steps')
        steps = []
        for dataStep in data.get('steps'):
            steps.append(LogBookStep.fromJson(dataStep))
        return LogBookTask(title, steps, created)
    
    def __str__(self):
        str = f'LogBookTask {self.title}'
        return str