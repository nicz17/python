"""
 A task with a number of steps
 and a title and description.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging

class Task:
    log = logging.getLogger(__name__)

    def __init__(self, title: str, desc: str, nStepsTotal: int):
        self.title = title
        self.desc = desc
        self.nStepsTotal = nStepsTotal
        self.nStepsDone = 0
        self.log.info('Constructor %s', self)

    def load(self):
        """Load the initial state of this task, if needed."""
        pass

    def inc(self):
        """Increment the task progress."""
        self.nStepsDone += 1

    def __str__(self):
        str = f'Task {self.title} at {self.nStepsDone}/{self.nStepsTotal}'
        return str