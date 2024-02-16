#!/usr/bin/env python3

"""
 Simple TODOlist app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from BaseApp import *
from LogBook import *
from LogBookTask import *


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
        if self.book is not None and len(self.book.tasks) == 0:
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
            self.log.info('Adding test tasks to %s', self.book)
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
    return logging.getLogger('LogBookApp')


def main():
    """Main function. Runs the app."""
    log.info('Welcome to LogBookApp v' + __version__)
    app = LogBookApp()
    app.run()

log = configureLogging()
#dOptions = getOptions()
main()
