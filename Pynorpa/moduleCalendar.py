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
        """Load calendar data."""
        week0 = datetime.date(year, month, 1).isocalendar()[1]
        self.log.info(f'Loading calendar data for {year}.{month}')
        for iDay, name in enumerate(self.dayNames):
            lblHeader = ttk.Label(self.frmMain, text=name)
            lblHeader.grid(column=iDay, row=0, padx=4, pady=8)
        for day in self.cal.itermonthdates(year, month):
            week = day.isocalendar()[1]
            lblDay = ttk.Label(self.frmMain, text=day.strftime('%d.%m'))
            if day.month != month:
                lblDay.configure(foreground='#c4c4c4')
            lblDay.grid(column=day.weekday(), row=week-week0+1, padx=4, pady=8)
        sMonth = TextTools.upperCaseFirst(DateTools.aMonthFr[month-1])
        self.frmMain.configure(text=f'{sMonth} {year}')

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