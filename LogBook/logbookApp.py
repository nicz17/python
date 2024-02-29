#!/usr/bin/env python3

"""
 Simple TODOlist app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import filedialog as fd
from BaseApp import *
from LogBook import *
from LogBookTask import *
from TaskList import *
from TextInputBox import *
from StepsTable import *
from StepEditor import *
from TaskEditor import *
from Importer import *
from Exporter import *


class LogBookApp(BaseApp):
    """LogBook App window."""
    log = logging.getLogger('LogBookApp')

    def __init__(self) -> None:
        """Constructor."""
        LogBook.initDefaultDir()
        self.iHeight = 800
        self.iWidth  = 1300
        self.book = None
        self.task = None
        self.step = None
        self.taskList = TaskList(self.onTaskSelection)
        self.taskInput = TextInputBox(self.addTask)
        self.stepInput = TextInputBox(self.addStep)
        self.stepsTable = StepsTable(self.onStepSelection)
        self.stepEditor = StepEditor(self.onStepSave)
        self.taskEditor = TaskEditor(self.onTaskSave)
        geometry = f'{self.iWidth}x{self.iHeight}'
        super().__init__('LogBook', geometry)
        self.loadBook()
        self.renderBook()

    def loadBook(self):
        """Load the default logbook."""
        self.log.info('Loading the default logbook')
        self.book = LogBook('TodoList')

    def renderBook(self):
        """Update rendering for the current book."""
        self.taskList.loadData(self.book)
        if self.book is not None:
            self.lblBook.configure(text = self.book.name)
            self.setStatus(f'Opened {self.book.getFilename()}')

    def renderTask(self):
        """Update rendering for the current task."""
        if self.task is None:
            self.lblTasks.configure(text = 'Tasks table')
        else:
            self.lblTasks.configure(text = self.task.title)

    def addTask(self, input: str):
        """Add a task from text input widget."""
        self.log.info('Adding task from user input')
        self.log.info('Task is %s', input)
        if self.book is not None and input is not None and len(input) > 0:
            self.book.addTask(LogBookTask(input))
            self.book.save()
            self.taskInput.clear()
            self.renderBook()
        else:
            self.log.info('Skipping empty input')

    def addStep(self, input: str):
        """Add a step from text input widget."""
        self.log.info('Adding Step %s', input)
        if self.task is not None and input is not None and len(input) > 0:
            self.task.addStep(LogBookStep(input))
            self.book.save()
            self.stepInput.clear()
            self.stepsTable.loadData(self.task)
        else:
            self.log.info('Skipping empty input')

    def onTaskSelection(self, evt):
        """TaskList selection handling."""
        sel = self.taskList.getSelection()
        if sel:
            self.task = sel
            self.log.info('Task selection: %s', self.task)
            self.renderTask()
            self.stepsTable.loadData(self.task)
            self.taskEditor.loadData(self.task)

    def onStepSelection(self, evt):
        """Step table selection handling."""
        idx = self.stepsTable.getSelection()
        if idx is None:
            self.step = None
        else:
            self.step = self.task.steps[idx]
        self.log.info('Step selection: %s', self.step)
        self.stepEditor.loadData(self.step)

    def onTaskSave(self):
        """Task save callback."""
        if self.book is not None:
            self.book.save()
            self.renderBook()
        self.taskEditor.loadData(self.task)

    def onStepSave(self):
        """Step save callback."""
        if self.book is not None:
            self.book.save()
        self.stepsTable.loadData(self.task)

    def onOpenFile(self):
        """Display dialog to open book from file."""
        filename = fd.askopenfilename(
            title = 'Open a LogBook',
            initialdir = LogBook.dir,
            filetypes = [('LogBook files', '*.logbook')])
        if filename:
            self.log.info('Loading %s', filename)
            self.book = LogBook(os.path.basename(filename).replace('.logbook', ''))
            self.stepEditor.loadData(None)
            self.stepsTable.loadData(None)
            self.renderBook()

    def onRefresh(self):
        """Refresh current display."""
        if self.book is not None:
            self.renderBook()

    def onImportFile(self):
        """Display dialog to import book from text file."""
        filename = fd.askopenfilename(
            title = 'Import from text file',
            initialdir = LogBook.dir,
            filetypes = [('Text files', '*.txt')])
        if filename:
            self.log.info('Importing %s', filename)
            importer = Importer()
            self.book = importer.importFromTextFile(filename)
            self.stepEditor.loadData(None)
            self.stepsTable.loadData(None)
            self.renderBook()

    def onExportFile(self):
        """Display dialog to export book to text file."""
        filename = fd.asksaveasfilename(
            title = 'Export to text file',
            initialdir = LogBook.dir,
            filetypes = [('Text files', '*.txt')])
        if filename and self.book:
            self.log.info('Exporting to %s', filename)
            exporter = Exporter()
            exporter.exportToTextFile(self.book, filename)


    def createWidgets(self):
        # Buttons
        self.addButton('Open',    self.onOpenFile)
        self.addButton('Refresh', self.onRefresh)
        self.addButton('Import',  self.onImportFile)
        self.addButton('Export',  self.onExportFile)

        # Frames
        self.frmBook = tk.Frame(master=self.frmMain,  width=300)#, bg='#f0f0ff')
        self.frmBook.pack(fill=tk.Y, side=tk.LEFT, pady=5)
        self.frmTasks = tk.Frame(master=self.frmMain, width=500)#, bg='#f0fff0')
        self.frmTasks.pack(fill=tk.Y, side=tk.LEFT, padx=5, pady=5)
        self.frmEdit = tk.Frame(master=self.frmMain,  width=300)#, bg='#fff0f0')
        self.frmEdit.pack(fill=tk.Y, side=tk.LEFT, pady=5)

        # LogBook title label
        self.lblBook = tk.Label(self.frmBook, width=21, 
            text='LogBook title', font='Helvetica 16 bold')
        self.lblBook.pack()

        # Task Listbox widget
        self.taskList.build(self.frmBook)
        
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

        # Task editor
        self.taskEditor.build(self.frmEdit)

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
