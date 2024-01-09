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
        self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.log.info('Constructor')
        self.canvas = canvas
        self.root = root
        self.width = 600

    def drawTasks(self, tasks):
        """Draw the specified tasks on the canvas."""
        iTask = 0
        for task in tasks:
            self.drawTask(task, iTask)
            iTask += 1

    def drawTask(self, task: Task, iTask: int):
        """Draw the specified task on the canvas."""
        sx = 10
        sy = iTask*100 + 10
        self.canvas.create_rectangle(sx, sy, sx+self.width, sy+90, outline = self.colorGridLines)
        self.canvas.create_text(sx+5, sy+15, text = task.title, anchor = 'w', font = self.fontBold)
        self.canvas.create_text(sx+5, sy+35, text = task.desc,  anchor = 'w')