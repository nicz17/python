"""
 A TabsApp Demo for testing.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
from TabsApp import TabsApp, TabModule
from BaseTable import AdvTable, TableColumn
from BaseTree import BaseTree
from BaseWidgets import SearchBar
from NameGen import NameGen


class DataDemo:
    def __init__(self, idx: int, name: str, desc: str):
        self.idx = idx
        self.name = name
        self.desc = desc

    def getName(self):
        return self.name
    
    def getDesc(self):
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

class ModuleTableDemo(TabModule):
    log = logging.getLogger('ModuleTableDemo')

    def __init__(self, oParent):
        self.table = TableDemo(self.onSelection)
        self.nameGen = NameGen()
        super().__init__(oParent, 'AdvTable')

    def onSelection(self, obj: DataDemo):
        self.log.info(f'Selected {obj}')

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
        self.log.info('Create widgets')
        self.createLeftRightFrames()
        self.tree.createWidgets(self.frmLeft)

    def populate(self, depth: int, parentId: str):
        for i in range(3):
            id = f'{parentId}-{i}' if parentId else str(i)
            self.tree.addItem(id, f'Level {depth} Item {id}', parentId)
            if depth < 3:
                self.populate(depth+1, id)

    def loadData(self):
        self.log.info('Load data')
        self.populate(1, None)

class AppDemo(TabsApp):
    def __init__(self):
        super().__init__('Demo TabsApp')
        self.tableDemo = ModuleTableDemo(self)
        self.treeDemo  = ModuleTreeDemo(self)


def main():
    app = AppDemo()
    app.run()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    main()
