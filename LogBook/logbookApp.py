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
from TextInputBox import *
from StepsTable import *
from StepEditor import *


class LogBookApp(BaseApp):
    """LogBook App window."""
    log = logging.getLogger('LogBookApp')

    def __init__(self) -> None:
        """Constructor."""
        self.iHeight = 800
        self.iWidth  = 1300
        self.book = None
        self.task = None
        self.step = None
        self.taskInput = TextInputBox(self.addTask)
        self.stepInput = TextInputBox(self.addStep)
        self.stepsTable = StepsTable(self.onStepSelection)
        self.stepEditor = StepEditor(self.onStepSave)

        geometry = f'{self.iWidth}x{self.iHeight}'
        super().__init__('LogBook', geometry)
        self.loadBook()
        self.renderBook()

    def loadBook(self):
        """Load the default logbook."""
        self.log.info('Loading the default logbook')
        self.book = LogBook('TestBook')

    def renderBook(self):
        """Update rendering for the current book."""
        self.listTasks.delete(0, tk.END)
        if self.book is not None:
            self.lblBook.configure(text = self.book.title)
            idx = 1
            task: LogBookTask
            for task in self.book.tasks:
                self.listTasks.insert(idx, task.title)
                idx += 1

    def renderTask(self):
        """Update rendering for the current task."""
        if self.task is None:
            self.lblTasks.configure(text = 'Tasks table')
        else:
            self.lblTasks.configure(text = self.task.title)

    def addTask(self):
        """Add a task from text input widget."""
        self.log.info('Adding task from user input')
        input = self.taskInput.getContent()
        self.log.info('Task is %s', input)
        if self.book is not None and input is not None and len(input) > 0:
            self.book.addTask(LogBookTask(input))
            self.book.save()
            self.taskInput.clear()
            self.renderBook()
        else:
            self.log.info('Skipping empty input')

    def addStep(self):
        """Add a step from text input widget."""
        self.log.info('Adding step from user input')
        input = self.stepInput.getContent()
        self.log.info('Step is %s', input)
        if self.task is not None and input is not None and len(input) > 0:
            self.task.addStep(LogBookStep(input))
            self.book.save()
            self.stepInput.clear()
            self.stepsTable.loadData(self.task)
        else:
            self.log.info('Skipping empty input')

    def onTaskSelection(self, evt):
        """Task ListBox selection handling."""
        if len(self.listTasks.curselection()) == 0:
            return
        index = int(self.listTasks.curselection()[0])
        self.task = self.book.tasks[index]
        self.log.info('Task selection: %d %s', index, self.task)
        self.renderTask()
        self.stepsTable.loadData(self.task)

    def onStepSelection(self, evt):
        """Step table selection handling."""
        idx = self.stepsTable.getSelection()
        if idx is None:
            self.step = None
        else:
            self.step = self.task.steps[idx]
        self.log.info('Step selection: %s', self.step)
        self.stepEditor.loadData(self.step)

    def onStepSave(self):
        if self.book is not None:
            self.book.save()
        #self.stepEditor.loadData(self.step)
        self.stepsTable.loadData(self.task)

    def createWidgets(self):
        # Frames
        self.frmBook = tk.Frame(master=self.frmMain,  width=300, bg='#f0f0ff')
        self.frmBook.pack(fill=tk.Y, side=tk.LEFT)
        self.frmTasks = tk.Frame(master=self.frmMain, width=400, bg='#f0fff0')
        self.frmTasks.pack(fill=tk.Y, side=tk.LEFT)
        self.frmEdit = tk.Frame(master=self.frmMain,  width=300, bg='#fff0f0')
        self.frmEdit.pack(fill=tk.Y, side=tk.LEFT)

        # LogBook title label
        self.lblBook = tk.Label(self.frmBook, width=21, 
            text='LogBook title', font='Helvetica 16 bold')
        self.lblBook.pack()

        # Task Listbox widget
        self.listTasks = tk.Listbox(self.frmBook, 
            height = 30, width = 32, 
            bg = "white", fg = "black",
            activestyle = 'dotbox', font = "Helvetica")
        self.listTasks.bind('<<ListboxSelect>>', self.onTaskSelection)
        self.listTasks.pack()
        
        # Task input TextBox
        self.window.update()
        self.taskInput.build(self.frmBook)

        # Steps title label
        self.lblTasks = tk.Label(self.frmTasks, width=38, 
            text='Steps table', font='Helvetica 16 bold')
        self.lblTasks.pack()

        # Steps table
        self.stepsTable.build(self.frmTasks)
        
        # Step input TextBox 
        self.stepInput.build(self.frmTasks)

        # Edition title label
        self.lblEdit = tk.Label(self.frmEdit, width=30, 
            text='Edition', font='Helvetica 16 bold')
        self.lblEdit.pack()

        # Step editor
        self.stepEditor.build(self.frmEdit)


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
