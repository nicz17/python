"""
 Pynorpa Module for calendar view of observations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.1"

import datetime
import logging
from tkinter import ttk

from BaseWidgets import MonthYearSelector
from calendarWidget import CalendarItem, CalendarWidget
from imageWidget import MultiImageWidget
from TabsApp import TabsApp, TabModule
from journal import Journal, JournalItem


class ModuleCalendar(TabModule):
    """Pynorpa Module for backup tasks."""
    log = logging.getLogger('ModuleCalendar')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.monthYearSel = MonthYearSelector(self.loadData)
        self.calWidget = CalendarWidget(self.onSelectItem)
        self.imgWidget = MultiImageWidget(None, None)
        super().__init__(parent, 'Calendrier')

    def loadData(self):
        """Load calendar data."""
        self.onSelectItem(None)
        month = self.monthYearSel.getMonth()
        year  = self.monthYearSel.getYear()
        self.calWidget.loadData(year, month)

        # Fetch Journal items
        dStart = datetime.date(year, month, 1)
        dEnd   = dStart + datetime.timedelta(days=31)
        self.log.info(f'Loading Journal for {year}.{month}')
        journal = Journal(dStart, dEnd)
        journalItems = journal.getJournalItems()
        for day in journalItems.keys():
            for idxLoc in journalItems[day].keys():
                widget = JournalItemWidget(journalItems[day][idxLoc], self.onSelectItem)
                self.calWidget.addItem(day.date(), widget)

    def onSelectItem(self, item: JournalItem):
        """Display pics of selected JournalItem in image widget."""
        if item:
            day = item.dtAt.strftime('%d.%m.%Y')
            self.lblTitle.config(text=f'Observations à {item.location.getName()} le {day}')
            self.imgWidget.loadImages(item.getPictures())
        else:
            self.lblTitle.config(text='')
            self.imgWidget.loadImages([])

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.monthYearSel.createWidgets(self.frmLeft)
        self.calWidget.createWidgets(self.frmLeft)
        self.lblTitle = ttk.Label(self.frmRight, text='', font='Helvetica 14 bold')
        self.lblTitle.pack(pady=6)
        self.imgWidget.createWidgets(self.frmRight)

    def __str__(self):
        return 'ModuleCalendar'

class JournalItemWidget(CalendarItem):
    """Widget displaying a clickable JournalItem in the calendar grid."""
    log = logging.getLogger('JournalItemWidget')

    def __init__(self, item: JournalItem, cbkSelection):
        super().__init__(item, cbkSelection)

    def getLabel(self):
        """Gets the label to display on calendar."""
        return self.item.getLabel()


def testModuleCalendar():
    print('Testing calendar module')
    app = TabsApp('Test calendar')
    ModuleCalendar(app)
    app.run()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testModuleCalendar()