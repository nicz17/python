"""
 Rendering methods for Pynorpa.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import font as tkfont
import logging
from BaseApp import *
from Task import *

class Renderer:
    """Rendering methods for Pynorpa."""
    colorGridLines = '#b0e0e0'
    log = logging.getLogger('Renderer')

    def __init__(self, canvas: tk.Canvas, root: tk.Tk):
        """Constructor. Initialise sizes and fonts."""
        self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.log.info('Constructor')
        self.canvas = canvas
        self.root = root
        self.width = 600

    def drawTasks(self, tasks):
        """Draw the specified tasks on the canvas."""
        self.canvas.delete('all')
        iTask = 0
        for task in tasks:
            self.drawTask(task, iTask)
            iTask += 1

    def drawTask(self, task: Task, iTask: int):
        """Draw the specified task on the canvas."""
        sx = 10
        sy = iTask*100 + 10
        colorTask = 'red'
        if task.isOver():
            colorTask = 'green'
        self.canvas.create_rectangle(sx, sy, sx+self.width, sy+90, outline = self.colorGridLines)
        self.canvas.create_oval(sx+5,  sy+15, sx+40, sy+50, fill=colorTask)
        self.canvas.create_text(sx+55, sy+15, text = task.title, anchor = 'w', font = self.fontBold)
        self.canvas.create_text(sx+55, sy+35, text = task.desc,  anchor = 'w')
        self.canvas.create_text(sx+55, sy+55, text = task.getStatus(), anchor = 'w')

    def __str__(self):
        return 'Renderer for Pynorpa tasks'