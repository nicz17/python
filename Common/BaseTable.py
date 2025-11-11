"""
Superclass for table widget, using a Ttk Treeview.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
from BaseWidgets import IconButton


class BaseTable():
    """A table widget."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSelectRow, objectLabel = 'rows'):
        """Constructor with row selection callback."""
        self.log.info('Constructor')
        self.cbkSelectRow = cbkSelectRow
        self.objectlabel = objectLabel
        self.data = []
        self.nRows = 0

    def onRowSelection(self, event = None):
        """Row selection callback."""
        idxRow = self.getSelectedRow()
        if self.cbkSelectRow:
            self.cbkSelectRow(self.data[idxRow] if idxRow is not None else None)
        
    def createWidgets(self, parent: ttk.Frame, columns):
        """Create user widgets."""
        self.tree = ttk.Treeview(parent, height=36)
        self.tree['columns'] = columns

        # Define columns
        self.tree.column('#0', width=0, stretch=tk.NO)
        for sColName in columns:
            self.tree.column(sColName, anchor=tk.W)

        # Define headings
        self.tree.heading('#0', text='', anchor=tk.W)
        for sColName in columns:
            self.tree.heading(sColName, text=sColName, anchor=tk.W)

        self.tree.bind('<<TreeviewSelect>>', self.onRowSelection)
        self.tree.pack(pady=5, anchor=tk.W)

        # Status and toolbar frame
        self.frmToolBar = ttk.Frame(parent, relief=tk.RAISED)
        self.frmToolBar.pack(fill=tk.X, side=tk.TOP)
        #self.toolbar = ttk.Frame(self.frmLeft, relief=tk.RAISED)
        #self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.lblStatus = ttk.Label(master=self.frmToolBar)
        self.lblStatus.pack(fill=tk.X, side=tk.LEFT) 

    def addRow(self, rowData):
        """Add a row to this table."""
        idx = self.nRows
        self.tree.insert(parent='', index='end', iid=idx, text='', values=rowData)
        self.nRows += 1
        self.setStatus(f'{self.nRows} {self.objectlabel}')

    def getSelectedRow(self) -> int:
        """Get the selected row index."""
        sel = self.tree.focus()
        #self.log.info('Table selection: %s', sel)
        if len(sel) == 0:
            return None
        else:
            return int(sel)
        
    def setStatus(self, text: str):
        """Set the status label message."""
        if text is None:
            text = ''
        self.lblStatus.configure(text=text)
        
    def clear(self):
        """Clears the tree contents."""
        self.tree.delete(*self.tree.get_children())
        self.nRows = 0
        self.setStatus(f'No {self.objectlabel}')

    def __str__(self) -> str:
        return f'BaseTable for {self.objectlabel}'

class TableColumn():
    """A table column."""
    log = logging.getLogger('TableColumn')

    def __init__(self, label: str, mtdGetter, width=100):
        """Constructor with label, getter method, and width in pixels."""
        self.label = label
        self.mtdGetter = mtdGetter
        self.width = width
    
class TableWithColumns(BaseTable):
    """A table configured with columns."""
    log = logging.getLogger('TableWithColumns')

    def __init__(self, cbkSelectRow, objectLabel = 'rows'):
        super().__init__(cbkSelectRow, objectLabel)
        self.columns = []

    def addColumn(self, column: TableColumn):
        """Add a column definition to this table."""
        self.columns.append(column)

    def getColumns(self) -> list[TableColumn]:
        """Get all columns of this table."""
        return self.columns
        
    def createWidgets(self, parent: tk.Frame, height=40):
        """Create user widgets."""

        # Scrolling frame
        frmScroll = ttk.Frame(parent)
        frmScroll.pack(pady=5, anchor=tk.W)

        # Treeview
        self.tree = ttk.Treeview(frmScroll, height=height)
        self.tree['columns'] = [col.label for col in self.getColumns()]
        self.tree.bind('<<TreeviewSelect>>', self.onRowSelection)
        
        # Scroll bar
        self.scrollbar = ttk.Scrollbar(frmScroll, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # Define columns
        self.tree.column('#0', width=0, stretch=tk.NO)
        for col in self.getColumns():
            self.tree.column(col.label, width=col.width, anchor=tk.W)

        # Define headings
        self.tree.heading('#0', text='', anchor=tk.W)
        for col in self.getColumns():
            self.tree.heading(col.label, text=col.label, anchor=tk.W)

        # Pack
        self.tree.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Status and toolbar frame
        self.frmToolBar = ttk.Frame(parent)
        self.frmToolBar.pack(fill=tk.X, anchor=tk.W)
        self.lblStatus = ttk.Label(master=self.frmToolBar)
        self.lblStatus.pack(fill=tk.X, side=tk.LEFT) 

    def addRows(self, data):
        """Add on table row for each object in data."""
        for object in data:
            self.addObject(object)

    def addObject(self, object):
        """Add a single object as a table row."""
        rowdata = []
        for col in self.getColumns():
            rowdata.append(col.mtdGetter(object))
        self.addRow(rowdata)

    def updateObject(self, object):
        """Update the selected row with the specified object."""
        #tree.item(iid, values=(new, values, here))
        iid = self.getSelectedRow()
        self.log.info(f'Will update row {iid}')
        rowdata = []
        for col in self.getColumns():
            rowdata.append(col.mtdGetter(object))
        self.tree.item(iid, values=rowdata)

        
class AdvTable(TableWithColumns):
    """Tests for table with title and toolbar, search etc."""
    log = logging.getLogger('AdvTable')

    def __init__(self, cbkSelectRow, objectLabel='rows', pady=0):
        self.pady = pady
        super().__init__(cbkSelectRow, objectLabel)
        self.addColumns()

    def addColumns(self):
        """Define the table columns."""
        pass

    def addRefreshButton(self, cbkRefresh):
        """Add an icon button to refresh table contents."""
        self.btnRefresh = IconButton(self.frmToolBar, 'refresh', 'Recharger la table', cbkRefresh, 6)

    def loadData(self, rows):
        """Display the specified rows in this table."""
        self.clear()
        self.data = rows
        self.addRows(rows)
        
    def setStatus(self, text: str):
        """Set the title bar text."""
        self.lblTitle.configure(text=f'{self.objectlabel} ({self.nRows})')

    def selectByIdx(self, idx):
        """Set selection by object index (not row number)."""
        self.log.info(f'Selecting object with idx {idx}')
        for idxRow, obj in enumerate(self.data):
            if obj.getIdx() == idx:
                self.tree.see(idxRow)
                self.tree.focus(idxRow)
                self.tree.selection_set(idxRow)
                return

    def createWidgets(self, parent: tk.Frame, height=40):
        """Create user widgets."""

        # Title bar
        self.lblTitle = ttk.Label(master=parent, text=f'Table for {self.objectlabel}', 
                                  #background='#ece8e4', 
                                  borderwidth=1, relief="groove")
        self.lblTitle.pack(fill=tk.X, side=tk.TOP, pady=(self.pady, 0))

        # Scrolling frame
        frmScroll = ttk.Frame(parent)
        frmScroll.pack(pady=0, anchor=tk.W)

        # Treeview
        self.tree = ttk.Treeview(frmScroll, height=height)
        self.tree['columns'] = [col.label for col in self.getColumns()]
        self.tree.bind('<<TreeviewSelect>>', self.onRowSelection)
        
        # Scroll bar
        self.scrollbar = ttk.Scrollbar(frmScroll, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # Define columns
        self.tree.column('#0', width=0, stretch=tk.NO)
        for col in self.getColumns():
            self.tree.column(col.label, width=col.width, anchor=tk.W)

        # Define headings
        self.tree.heading('#0', text='', anchor=tk.W)
        for col in self.getColumns():
            self.tree.heading(col.label, text=col.label, anchor=tk.W)

        # Pack
        self.tree.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Toolbar frame
        self.frmToolBar = ttk.Frame(parent)
        self.frmToolBar.pack(fill=tk.X, anchor=tk.W)