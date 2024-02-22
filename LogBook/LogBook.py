"""
A LogBook for the app of the same name.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
import time
import json
import DateTools
from pathlib import Path
from LogBookTask import *


class LogBook():
    """A list of tasks and steps."""
    log = logging.getLogger('LogBook')
    dir = None

    def __init__(self, name: str) -> None:
        """Constructor with name."""
        self.name = name
        self.title = 'Default LogBook'
        self.created = time.time()
        self.tasks = []
        self.log.info('Constructor %s', self)
        self.load()

    def addTask(self, task: LogBookTask):
        """Add the specified task to this LogBook."""
        if task is not None:
            self.tasks.append(task)

    def clear(self):
        """Remove all tasks from this book."""
        self.tasks = []

    def load(self):
        """Load from a JSON file or create new if no file."""
        filename = self.getFilename()
        if os.path.exists(filename):
            self.log.info('Loading from %s', filename)
            self.fromJson()
        else:
            self.log.info('Creating new %s', self)
            self.toJson()

    def save(self):
        """Save this LogBook as a JSON file."""
        filename = self.getFilename()
        self.log.info('Saving as %s', filename)
        file = open(filename, 'w')
        file.write(json.dumps(self.toJson(), indent=2))
        file.close()

    def getFilename(self):
        """Get this book's file name."""
        return f'{LogBook.dir}{self.name}.logbook'

    def toJson(self):
        """Export this LogBook as JSON."""
        dataTasks = []
        for task in self.tasks:
            dataTasks.append(task.toJson())
        data = {
            'class': type(self).__name__,
            'version': __version__,
            'name': self.name,
            'title': self.title,
            'created': DateTools.timestampToString(self.created),
            'tasks': dataTasks
        }
        return data

    def fromJson(self):
        """Load data from a JSON file."""
        filename = self.getFilename()
        file = open(filename, 'r')
        data = json.load(file)
        file.close()

        self.title = data.get('title')
        self.created = DateTools.stringToTimestamp(data.get('created'))
        for dataTask in data.get('tasks'):
            self.tasks.append(LogBookTask.fromJson(dataTask))
        self.log.info('Loaded from JSON with title %s', self.title)

    def __str__(self):
        str = f'LogBook {self.name}'
        return str
    
    @staticmethod
    def initDefaultDir():
        """Set the default directory for LogBook files."""
        home = str(Path.home())
        LogBook.dir = f'{home}/Documents/LogBook/'
        LogBook.log.info('Default directory: %s', LogBook.dir)
