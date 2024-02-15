#!/usr/bin/env python3

"""
 Simple TODOlist app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import os
import sys
import logging
import getopt
import time
import json
import DateTools
import tkinter as tk
from BaseApp import *
from LogBookTask import *


class LogBook():
    """A list of tasks and steps."""
    log = logging.getLogger('LogBook')

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

    def load(self):
        """Load from a JSON file or create new if no file."""
        filename = f'{self.name}.json'
        if os.path.exists(filename):
            self.log.info('Loading from %s', filename)
            self.fromJson()
        else:
            self.log.info('Creating new %s', self)
            self.toJson()

    def toJson(self):
        """Save this LogBook as a JSON file."""
        filename = f'{self.name}.json'
        dataTasks = []
        for task in self.tasks:
            dataTasks.append(task.toJson())
        data = {
            'name': self.name,
            'title': self.title,
            'created': DateTools.timestampToString(self.created),
            'tasks': dataTasks
        }
        self.log.info('Saving as %s', filename)
        file = open(filename, 'w')
        file.write(json.dumps(data, indent=2))
        file.close()

    def fromJson(self):
        """Load data from a JSON file."""
        filename = f'{self.name}.json'
        file = open(filename, 'r')
        data = json.load(file)
        file.close()

        self.title = data.get('title')
        self.created = DateTools.stringToTimestamp(data.get('created'))
        #self.tasks = data.get('tasks')
        for dataTask in data.get('tasks'):
            self.tasks.append(LogBookTask.fromJson(dataTask))
        self.log.info('Loaded from JSON with title %s', self.title)

    def __str__(self):
        str = f'LogBook {self.name}'
        return str

class LogBookApp(BaseApp):
    """LogBook App window."""
    log = logging.getLogger('LogBookApp')

    def __init__(self) -> None:
        """Constructor."""
        self.iHeight = 800
        self.iWidth  = 1000
        self.book = None
        sGeometry = f'{self.iWidth}x{self.iHeight}'
        super().__init__('LogBook', sGeometry)
        self.loadBook()
        self.addTestTasks()

    def loadBook(self):
        """Load the default logbook."""
        self.log.info('Loading the default logbook')
        self.book = LogBook('TestBook')

        idx = 1
        for task in self.book.tasks:
            self.listTasks.insert(idx, task.title)
            idx += 1

    def addTestTasks(self):
        """Add some test tasks to the default book."""
        if self.book is not None:
            self.book.addTask(LogBookTask('Buy some bread'))
            self.book.addTask(LogBookTask('Build a Golem deck'))
            self.book.toJson()

    def createWidgets(self):
        # create listbox object
        self.listTasks = tk.Listbox(self.window, 
            height = 10, width = 20, 
            bg = "white", fg = "black",
            activestyle = 'dotbox', font = "Helvetica")
        self.listTasks.pack()

def configureLogging():
    """
    Configures logging to have timestamped logs at INFO level
    on stdout and in a log file.
    """
    
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s %(name)s: %(message)s',
        datefmt = '%Y.%m.%d %H:%M:%S',
        level = logging.INFO,
        handlers = [
            #logging.FileHandler("logbook.log"),
            logging.StreamHandler()
        ])
    return logging.getLogger('LogBook')


def main():
    """Main function. Runs the app."""
    log.info('Welcome to LogBook v' + __version__)

    app = LogBookApp()
    app.run()

log = configureLogging()
#dOptions = getOptions()
main()
