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
    Todo = 0
    Idle = 1
    Done = 2
    Fail = 3

    def getColor(self):
        """Get the hex color code for the status."""
        color = '#ffffd0'
        if self == Status.Done:
            color = '#d0ffd0'
        if self == Status.Fail:
            color = '#ffd0d0'
        return color

    def __str__(self):
        return self.name
    
class LogBookStep:
    """A step in a LogBook task."""
    log = logging.getLogger(__name__)

    def __init__(self, text: str, status=None, order=0):
        """Constructor with text, status."""
        self.text = text
        if status is None:
            status = Status.Todo
        self.status = status
        self.order = order

    def getText(self):
        return self.text
    
    def getStatusName(self):
        return self.status.name
    
    def getOrder(self):
        return self.order
    
    def getOrderStr(self):
        if self.order is None:
            return ''
        return self.order

    def toJson(self):
        """Export this step as JSON."""
        data = {
            'text': self.text,
            'status': self.status.name,
            'order': self.order
        }
        return data
    
    @staticmethod
    def fromJson(data):
        """Load data from a JSON object."""
        text  = data.get('text')
        order = data.get('order')
        status = Status[data.get('status')]
        return LogBookStep(text, status, order)
    
    def __lt__(self, other):
        if not isinstance(other, LogBookStep):
            return NotImplemented
        if self.status.value == other.status.value:
            if self.order == other.order:
                return self.text < other.text
            if self.order is not None and other.order is not None:
                return self.order < other.order
        return self.status.value > other.status.value
    
    def __str__(self):
        str = f'LogBookStep {self.text} {self.status}'
        return str


class LogBookTask:
    """A task with steps for the LogBook app."""
    log = logging.getLogger(__name__)

    def __init__(self, title, steps = None, created = None, status = None):
        """Constructor with title, steps, created timestamp."""
        self.title = title
        if created is None:
            created = time.time()
        self.created = created
        if steps is None:
            steps = []
        self.steps = steps
        if status is None:
            status = Status.Todo
        self.status = status

    def addStep(self, step: LogBookStep):
        """Add a step to this task."""
        if step is not None:
            step.order = self.getNextStepOrder()
            self.steps.append(step)
            self.updateStatus()

    def countSteps(self) -> int:
        """Count the number of steps in this task."""
        return len(self.steps)

    def countActiveSteps(self) -> int:
        """Count the number of active steps in this task."""
        nActive = 0
        for step in self:
            if step.status != Status.Done:
                nActive += 1
        return nActive

    def countDoneSteps(self) -> int:
        """Count the number of done steps in this task."""
        nDone = 0
        for step in self:
            if step.status == Status.Done:
                nDone += 1
        return nDone
    
    def getNextStepOrder(self) -> int:
        """Compute the next step order."""
        maxOrder = 0
        for step in self:
            if step.order is not None:
                maxOrder = max(maxOrder, step.order)
        return maxOrder+1
    
    def updateStatus(self):
        """Update task status based on steps status."""
        isDone = True
        for step in self:
            if step.status != Status.Done:
                isDone = False
            if step.status == Status.Fail:
                self.status = Status.Fail
                return
        if len(self.steps) > 0 and isDone:
            self.status = Status.Done
        else:
            self.status = Status.Todo
    
    def sort(self):
        """Sort the steps in this task."""
        self.steps = sorted(self.steps)

    def getTitle(self):
        return self.title
    
    def getStatusName(self):
        return self.status.name
    
    def getCreatedString(self):
        return DateTools.timestampToString(self.created)

    def toJson(self):
        """Export this task as JSON."""
        dataSteps = []
        for step in self:
            dataSteps.append(step.toJson())
        data = {
            'title': self.title,
            'created': DateTools.timestampToString(self.created),
            'status': self.status.name,
            'steps': dataSteps
        }
        return data
    
    @staticmethod
    def fromJson(data):
        """Load data from a JSON object."""
        title = data.get('title')
        created = DateTools.stringToTimestamp(data.get('created'))
        steps = []
        status = None
        if 'status' in data:
            status = Status[data.get('status')]
        for dataStep in data.get('steps'):
            steps.append(LogBookStep.fromJson(dataStep))
        return LogBookTask(title, sorted(steps), created, status)
    
    def __iter__(self):
        """Iterate on this task's steps."""
        step: LogBookStep
        for step in self.steps:
            yield step
    
    def __lt__(self, other):
        """Sort by status and creation date"""
        if not isinstance(other, LogBookTask):
            return NotImplemented
        if self.status.value == other.status.value:
            return self.created < other.created
        return self.status.value > other.status.value
    
    def __str__(self):
        str = f'LogBookTask {self.title}'
        return str