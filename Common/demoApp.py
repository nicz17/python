"""
 A TabsApp Demo for testing.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.2"

import datetime
import glob
import logging
import os
import DateTools
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from BaseTable import AdvTable, TableColumn
from BaseTree import BaseTree
from BaseWidgets import SearchBar, MonthYearSelector, IconButton, BaseEditor
from calendarWidget import CalendarWidget, CalendarItem
from mapWidget import MapWidget
from NameGen import NameGen
from TabsApp import TabsApp, TabModule


class DataDemo:
    """Container class for demo data."""
    def __init__(self, idx: int, name: str, desc: str):
        self.idx = idx
        self.name = name
        self.desc = desc

    def getIdx(self) -> str:
        return str(self.idx)

    def getName(self) -> str:
        return self.name
    
    def getDesc(self) -> str:
        return self.desc

    def __str__(self):
        return f'DataDemo {self.idx} {self.name} {self.desc}'

class TableDemo(AdvTable):
    log = logging.getLogger('TableDemo')

    def __init__(self, cbkSelection=None):
        super().__init__(cbkSelection, 'Demo data')

    def onSearch(self, search: str):
        """Search for data matching the specified text."""
        self.log.info(f'Searching for {search}')
        for idxRow, obj in enumerate(self.data):
            if search.lower() in obj.desc.lower():
                self.log.debug(f'  Found {obj} at {idxRow}')
                self.selectRow(idxRow)
                return
        self.log.info(f'No match for {search}')

    def addColumns(self):
        """Define the table columns."""
        self.log.info('Column config')
        self.addColumn(TableColumn('Nom', DataDemo.getName, 120))
        self.addColumn(TableColumn('Description', DataDemo.getDesc, 240))

class EditorDemo(BaseEditor):
    log = logging.getLogger('EditorDemo')

    def __init__(self, cbkSave=None, colorLabelDef='black'):
        super().__init__(cbkSave, colorLabelDef)

    def createWidgets(self, parent):
        super().createWidgets(parent, 'Propriétés')
        self.addTextReadOnly('Index', DataDemo.getIdx)
        self.addTextReadOnly('Nom', DataDemo.getName)
        self.addTextReadOnly('Description', DataDemo.getDesc)
        self.createButtons(True, True, True)

class ModuleTableDemo(TabModule):
    log = logging.getLogger('ModuleTableDemo')

    def __init__(self, oParent):
        self.nameGen = NameGen()
        self.table = TableDemo(self.onSelection)
        self.editor = EditorDemo()
        super().__init__(oParent, 'AdvTable')

    def onSelection(self, obj: DataDemo):
        self.log.info(f'Selected {obj}')
        self.editor.setValue(obj)
        self.editor.enableWidgets(obj is not None)

    def onCtxtMenuAction(self):
        sel = self.table.getSelectedRow()
        self.log.info(f'Context menu action {sel}')

    def createWidgets(self):
        self.log.info('Create widgets')
        self.createLeftRightFrames()

        self.table.createWidgets(self.frmLeft, 24)
        self.searchBar = SearchBar(self.table.frmToolBar, 36, self.table.onSearch)
        self.table.addRefreshButton(self.loadData)
        self.table.addContextMenu(self.oParent.window)
        self.table.addContextMenuAction('Details', self.onCtxtMenuAction)
        self.table.addContextMenuAction('Preview', self.onCtxtMenuAction)

        self.editor.createWidgets(self.frmRight)

    def loadData(self):
        self.log.info('Load data')
        data = []
        for i in range(20):
            data.append(DataDemo(i, f'DemoData{i:02d}', self.nameGen.generate()))
        self.table.loadData(data)
        #self.searchBar.enableWidget(True)

class ModuleTreeDemo(TabModule):
    log = logging.getLogger('ModuleTreeDemo')

    def __init__(self, oParent):
        self.tree = BaseTree(None)
        super().__init__(oParent, 'BaseTree')

    def createWidgets(self):
        self.createLeftRightFrames()
        self.tree.createWidgets(self.frmLeft)

    def populate(self, depth: int, parentId: str):
        for i in range(3):
            id = f'{parentId}-{i}' if parentId else str(i)
            self.tree.addItem(id, f'Level {depth} Item {id}', parentId)
            if depth < 3:
                self.populate(depth+1, id)

    def loadData(self):
        self.populate(1, None)

class ModuleCalendarDemo(TabModule):
    log = logging.getLogger('ModuleCalendarDemo')

    def __init__(self, oParent):
        self.selector = MonthYearSelector(self.onSelect)
        self.calendar = CalendarWidget(self.onItemSelection)
        self.lblSelected = None
        super().__init__(oParent, 'CalendarWidget')

    def onSelect(self):
        self.loadData()

    def onItemSelection(self, item=None):
        if item:
            self.lblSelected.config(text=item)
        else:
            self.lblSelected.config(text='')

    def loadData(self):
        month = self.selector.getMonth()
        year  = self.selector.getYear()
        self.calendar.loadData(year, month)
        self.addCalendarItem(datetime.date(year, month,  1), 'Calendes')
        self.addCalendarItem(datetime.date(year, month,  8), 'Nones')
        self.addCalendarItem(datetime.date(year, month, 15), 'Ides')

    def addCalendarItem(self, day: datetime.date, name: str):
        obj = DataDemo(0, name, name)
        item = CalendarItem(obj, self.onItemSelection)
        self.calendar.addItem(day, item)

    def createWidgets(self):
        self.createLeftRightFrames()
        self.selector.createWidgets(self.frmLeft)
        self.calendar.createWidgets(self.frmLeft)
        self.lblSelected = ttk.Label(self.frmLeft, text='')
        self.lblSelected.pack()

class ModuleIconsDemo(TabModule):
    log = logging.getLogger('ModuleIconsDemo')

    def __init__(self, oParent):
        super().__init__(oParent, 'Icons')
        self.path = f'{Path.home()}/prog/icons'
        self.maxCols = 6

    def onIconClick(self, file: str):
        self.log.info(f'Selected {file}')

    def createWidgets(self):
        self.createLeftRightFrames()

        # Init grid display
        row = 0
        col = 0

        # Find icon files
        files = glob.glob(f'{self.path}/*.png')
        files.sort()
        for file in files:
            self.log.debug(f'Adding {file}')
            icon = os.path.basename(file).removesuffix('.png')
            if col == self.maxCols:
                col = 0
                row += 1
            frame = ttk.Frame(self.frmLeft)
            frame.grid(row=row, column=col, pady=12)
            btn = IconButton(frame, icon, file, lambda file=file: self.onIconClick(file), 0, False)
            btn.lbl.grid(column=0, row=0)
            ttk.Label(frame, text=icon).grid(column=0, row=1)
            col += 1

        # Set grid cell sizes
        col_count, row_count = self.frmLeft.grid_size()
        for col in range(col_count):
            self.frmLeft.grid_columnconfigure(col, minsize=64)
        for row in range(1, row_count):
            self.frmLeft.grid_rowconfigure(row, minsize=32)

class DateToolsDemoData:
    """Demo data for DateTools methods."""
    log = logging.getLogger('ModuleDateToolsDemo')

    def __init__(self):
        self.start = DateTools.now()

    def getNowStr(self) -> str:
        return DateTools.nowAsString()

    def getNowUtc(self) -> str:
        dtNow = DateTools.timestampToDatetimeUTC(DateTools.now())
        return DateTools.datetimeToStringUTC(dtNow)

    def getMidnight(self) -> str:
        midnight = DateTools.datetimeToMidnight(DateTools.nowDatetime())
        return DateTools.datetimeToString(midnight)

    def getTomorrow(self) -> str:
        tmr = DateTools.addDays(DateTools.now(), 1)
        return DateTools.timestampToString(tmr)

    def getLocalised(self) -> str:
        return DateTools.datetimeToPrettyStringFr(DateTools.nowDatetime())

    def getDayOfYear(self) -> str:
        year = DateTools.nowDatetime().year
        dtYearStart = datetime.datetime(year, 1, 1)
        return str(DateTools.getDaysSince(dtYearStart)+1)

    def getNextDst(self) -> str:
        daysToDst = DateTools.timeUntilNextDSTSwitch()
        return f'In {daysToDst} days'

    def getUptime(self) -> str:
        elapsed = DateTools.now() - self.start
        return f'{elapsed:0.4f}s'
    
class EditorDateTools(BaseEditor):
    log = logging.getLogger('EditorDateTools')

    def __init__(self, cbkSave=None, colorLabelDef='black'):
        super().__init__(cbkSave, colorLabelDef)

    def createWidgets(self, parent):
        super().createWidgets(parent, 'DateTools methods')
        self.addTextReadOnly('Now local',   DateToolsDemoData.getNowStr)
        self.addTextReadOnly('Now UTC',     DateToolsDemoData.getNowUtc)
        self.addTextReadOnly('Midnight',    DateToolsDemoData.getMidnight)
        self.addTextReadOnly('Tomorrow',    DateToolsDemoData.getTomorrow)
        self.addTextReadOnly('Localised',   DateToolsDemoData.getLocalised)
        self.addTextReadOnly('Day of year', DateToolsDemoData.getDayOfYear)
        self.addTextReadOnly('DST switch',  DateToolsDemoData.getNextDst)
        self.addTextReadOnly('Uptime',      DateToolsDemoData.getUptime)

class ModuleDateToolsDemo(TabModule):
    log = logging.getLogger('ModuleDateToolsDemo')

    def __init__(self, oParent):
        self.data = DateToolsDemoData()
        self.editor = EditorDateTools()
        super().__init__(oParent, 'DateTools')
        self.refreshLoop()

    def refreshLoop(self):
        """Refresh the data every second."""
        self.loadData()
        self.schedule(1000, self.refreshLoop)

    def loadData(self):
        self.editor.setValue(self.data)
        self.editor.enableWidgets(True)

    def createWidgets(self):
        self.log.debug('Create widgets')
        self.createLeftRightFrames()
        self.editor.createWidgets(self.frmLeft)
        self.editor.enableWidgets(True)

class ModuleMapDemo(TabModule):
    log = logging.getLogger('ModuleMapDemo')

    def __init__(self, oParent):
        self.map = MapWidget()
        super().__init__(oParent, 'MapWidget')

    def loadData(self):
        self.map.loadData(None)

    def createWidgets(self):
        self.createLeftRightFrames()
        self.map.createWidgets(self.frmLeft, 6, 6)

class AppDemo(TabsApp):
    """Demo app for base widgets and other common classes."""
    def __init__(self):
        appIcon = f'{Path.home()}/prog/icons/ok.png'
        super().__init__('Demo TabsApp', '1200x800', appIcon)
        ModuleTableDemo(self)
        ModuleTreeDemo(self)
        ModuleCalendarDemo(self)
        ModuleIconsDemo(self)
        ModuleDateToolsDemo(self)
        ModuleMapDemo(self)


def main():
    app = AppDemo()
    app.run()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    main()
