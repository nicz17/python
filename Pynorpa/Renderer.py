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
from Palette import GreenRedPalette

class Renderer:
    """Rendering methods for Pynorpa."""
    colorGridLines = '#b0b0b0'
    log = logging.getLogger('Renderer')

    def __init__(self, canvas: tk.Canvas, root: tk.Tk):
        """Constructor. Initialise sizes and fonts."""
        self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.log.info('Constructor')
        self.palette = GreenRedPalette()
        self.canvas = canvas
        self.root = root
        self.width = 750

    def drawTasks(self, tasks):
        """Draw the specified tasks on the canvas."""
        self.canvas.delete('all')
        for count, task in enumerate(tasks):
            self.drawTask(task, count)

    def drawTask(self, task: Task, iTask: int):
        """Draw the specified task on the canvas."""
        sx = 10
        sy = iTask*105 + 10
        self.canvas.create_rectangle(sx, sy, sx+self.width, sy+96, outline = self.colorGridLines)
        self.canvas.create_oval(sx+8,  sy+15, sx+43, sy+50, fill=self.getTaskColor(task), outline="")
        self.canvas.create_text(sx+55, sy+15, text=task.title, anchor='w', font=self.fontBold)
        self.canvas.create_text(sx+55, sy+35, text=task.desc,  anchor='w')
        self.canvas.create_text(sx+55, sy+55, text=task.getStatus(), anchor='w')
        self.canvas.create_rectangle(sx+55, sy+70, sx+self.width-20, sy+87, fill='#a0a0a0', outline='')
        if task.nStepsTotal > 0 and task.nStepsDone > 0:
            widthProg = int((self.width-75)*task.nStepsDone/task.nStepsTotal)
            color = self.palette.getColorHex(1.0 - task.nStepsDone/task.nStepsTotal)
            self.canvas.create_rectangle(sx+55, sy+70, sx+55+widthProg, sy+87, fill=color, outline='')

    def getTaskColor(self, task: Task) -> str:
        """Get the color of the task icon."""
        color = '#ff4000'  # not started
        if task.nStepsTotal == 0:
            color = '#a0a0a0'  # undefined
        elif task.isOver():
            color = '#40ff00'  # done
        elif task.nStepsDone > 0:
            color = '#ffa500'  # ongoing
        return color

    def __str__(self):
        return 'Renderer for Pynorpa tasks'