"""
 Pynorpa Module for calendar view of observations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk

import calendar
import datetime
import DateTools
import TextTools

from BaseWidgets import MonthYearSelector
from TabsApp import TabsApp, TabModule
from journal import Journal


class ModuleCalendar(TabModule):
    """Pynorpa Module for backup tasks."""
    log = logging.getLogger('ModuleCalendar')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.monthYearSel = MonthYearSelector(self.loadData)
        self.calWidget = CalendarWidget(None)
        super().__init__(parent, 'Calendrier')

    def loadData(self):
        """Load calendar data."""
        self.calWidget.loadData(self.monthYearSel.getYear(), self.monthYearSel.getMonth())

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.monthYearSel.createWidgets(self.frmLeft)
        self.calWidget.createWidgets(self.frmLeft)

    def __str__(self):
        return 'ModuleCalendar'


class CalendarWidget:
    """Calendar grid widget."""
    log = logging.getLogger('CalendarWidget')
    dayNames = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    def __init__(self, cbkSelection):
        """Constructor."""
        self.cbkSelection = cbkSelection
        self.cal = calendar.TextCalendar()

    def loadData(self, year: int, month: int):
        """Load calendar data for the specified month."""
        dStart = datetime.date(year, month, 1)
        dEnd   = dStart + datetime.timedelta(days=31)
        week0 = dStart.isocalendar()[1]
        self.log.info(f'Loading calendar data for {year}.{month}')
        journal = Journal(dStart, dEnd)
        journalItems = journal.getJournalItems()

        # Clear the frame
        for widget in self.frmMain.winfo_children():
            widget.destroy()

        # Frame title and table headers
        sMonth = TextTools.upperCaseFirst(DateTools.aMonthFr[month-1])
        self.frmMain.configure(text=f'{sMonth} {year}')
        for iDay, name in enumerate(self.dayNames):
            lblHeader = ttk.Label(self.frmMain, text=name, background='#c4c4c4', anchor="center")
            lblHeader.grid(column=iDay, row=0, padx=4, pady=6, sticky='WE')

        # Table cells
        for day in self.cal.itermonthdates(year, month):
            week = day.isocalendar()[1]
            col = day.weekday()
            row = week-week0+1

            # Cell content and style
            lblDay = ttk.Label(self.frmMain, text=day.strftime('%d.%m'))
            if day.month != month:
                lblDay.configure(foreground='#c4c4c4')
            lblDay.grid(column=col, row=row, padx=4, pady=4, sticky='N')

            # Add JournalItems
            dtDay = datetime.datetime.combine(day, datetime.datetime.min.time())
            if dtDay in journalItems:
                for idxLoc in journalItems[dtDay].keys():
                    item = journalItems[dtDay][idxLoc]
                    # TODO add label click action with imageWidget
                    lblItem = ttk.Label(self.frmMain, text=item.getLabel())
                    lblItem.grid(column=col, row=row, padx=4, pady=8)
                    # FIXME fails if more than 1 item on same day

        # Set grid cell sizes
        col_count, row_count = self.frmMain.grid_size()
        for col in range(col_count):
            self.frmMain.grid_columnconfigure(col, minsize=150)
        for row in range(1, row_count):
            self.frmMain.grid_rowconfigure(row, minsize=80)


    def createWidgets(self, parent):
        """Create user widgets."""
        self.frmMain = ttk.LabelFrame(parent, text='CalendarWidget')
        self.frmMain.pack(pady=6)

    def __str__(self):
        return 'CalendarWidget'


def testModuleCalendar():
    print('Testing calendar module')
    app = TabsApp('Test calendar')
    ModuleCalendar(app)
    app.run()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testModuleCalendar()