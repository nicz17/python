"""
 Calendar widget.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk

import calendar
import datetime
import DateTools
import TextTools


class CalendarItem:
    """Widget displaying a clickable item in the calendar grid."""
    log = logging.getLogger('CalendarItem')
    colorLink = '#4200c0'

    def __init__(self, item, cbkSelection):
        self.item = item
        self.cbkSelection = cbkSelection
        self.lbl = None

    def onSelection(self, event=None):
        self.log.debug(f'Selected {self.item}')
        self.cbkSelection(self.item)

    def getLabel(self):
        """Gets the label to display on calendar."""
        return self.item.getDesc()

    def createWidgets(self, frame, pady=2):
        self.lbl = ttk.Label(frame, foreground=self.colorLink, 
                            cursor="hand1", text=self.getLabel())
        self.lbl.bind("<Button-1>", self.onSelection)
        self.lbl.pack(padx=3, pady=pady)

    def __str__(self):
        return f'CalendarItem {self.item}'

class CalendarWidget:
    """Calendar grid widget."""
    log = logging.getLogger('CalendarWidget')
    dayNames = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    def __init__(self, cbkSelection):
        """Constructor."""
        self.cbkSelection = cbkSelection
        self.cal = calendar.TextCalendar()
        self.dayFrames = {}

    def addItem(self, day: datetime.date, item: CalendarItem):
        """Adds a CalendarItem on the specified day."""
        if not day or not item:
            return
        frame = self.dayFrames[day]
        if frame:
            item.createWidgets(frame)
        else:
            self.log.error(f'Could not find frame for {day}')

    def loadData(self, year: int, month: int):
        """Load calendar data for the specified month."""
        dStart = datetime.date(year, month, 1)
        #dEnd   = dStart + datetime.timedelta(days=31)
        week0 = dStart.isocalendar()[1]
        self.log.info(f'Loading calendar data for {year}.{month}')

        # Clear the frame
        for widget in self.frmMain.winfo_children():
            widget.destroy()
        self.dayFrames = {}

        # Frame title and table headers
        sMonth = TextTools.upperCaseFirst(DateTools.aMonthFr[month-1])
        self.frmMain.configure(text=f'{sMonth} {year}')
        for iDay, name in enumerate(self.dayNames):
            lblHeader = ttk.Label(self.frmMain, text=name, background='#c4c4c4', anchor="center")
            lblHeader.grid(column=iDay, row=0, padx=3, pady=6, sticky='WE')

        # Table cells
        for day in self.cal.itermonthdates(year, month):
            week = day.isocalendar()[1]
            col = day.weekday()
            row = week-week0+1

            frmDay = ttk.Frame(self.frmMain)
            frmDay.grid(column=col, row=row, padx=1, pady=1, sticky='N')
            self.dayFrames[day] = frmDay

            # Cell content and style
            lblDay = ttk.Label(frmDay, text=day.strftime('%d'))
            if day.month != month:
                lblDay.configure(foreground='#c4c4c4', text=day.strftime('%d.%m'))
            #lblDay.grid(column=0, row=0, pady=4, sticky='N')
            lblDay.pack(pady=4, side=tk.TOP)

        # Set grid cell sizes
        col_count, row_count = self.frmMain.grid_size()
        for col in range(col_count):
            self.frmMain.grid_columnconfigure(col, minsize=150)
        for row in range(1, row_count):
            self.frmMain.grid_rowconfigure(row, minsize=100)

        # Add grid line separators
        style = ttk.Style()
        style.configure('Line.TSeparator', background='#a0a0a0')
        for col in range(1, col_count):
            sep = ttk.Separator(self.frmMain, style='Line.TSeparator', orient=tk.VERTICAL)
            sep.grid(column=col, row=0, rowspan=row_count, sticky='NSW', pady=6)
        for row in range(1, row_count-1):
            sep = ttk.Separator(self.frmMain, style='Line.TSeparator', orient=tk.HORIZONTAL)
            sep.grid(column=0, row=row, columnspan=col_count, sticky='SWE', padx=4)

    def createWidgets(self, parent):
        """Create user widgets."""
        self.frmMain = ttk.LabelFrame(parent, text='CalendarWidget')
        self.frmMain.pack(pady=6)

    def __str__(self):
        return 'CalendarWidget'
