"""
 Subclass of BaseApp with tabbed frames, using a ttk Notebook widget.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import ttk
import logging
from BaseApp import *

class TabsApp(BaseApp):
    """Subclass of BaseApp using tabbed frames."""
    log = logging.getLogger('TabsApp')

    def __init__(self, sTitle, sGeometry='1200x800', sIconFile=None) -> None:
        """Constructor with title and sizes."""
        self.dictTabs = {}
        super().__init__(sTitle, sGeometry, sIconFile)

    def createBaseWidgets(self):
        """Create base widgets"""
        self.frmTop = ttk.Frame(master=self.window, width=1200, height=800)
        self.frmTop.pack(fill=tk.BOTH, side=tk.TOP)
        self.frmButtons = ttk.Frame(master=self.frmTop, width=100, height=800)
        self.frmButtons.pack(fill=tk.Y, side=tk.LEFT)
        self.frmBottom = ttk.Frame(master=self.window, width=1200, height=50)
        self.frmBottom.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.tabControl = ttk.Notebook(self.frmTop, height=940)
        self.tabControl.pack(expand=1, fill=tk.BOTH, pady=3, padx=5)
        self.tabControl.bind("<<NotebookTabChanged>>", self.onTabSelection)

        self.lblStatus = ttk.Label(master=self.frmBottom)
        self.lblStatus.pack(fill=tk.X) 
        
    def addTab(self, oTab: 'TabModule'):
        """Add a TabModule object to our tabs. Returns the added frame."""
        self.log.info('Adding tab %s', oTab.getTitle())
        tab = ttk.Frame(self.tabControl)
        self.tabControl.add(tab, text = oTab.getTitle())
        self.dictTabs[oTab.getTitle()] = oTab
        return tab
    
    def navigate(self, idxTab: int):
        """Select tab with the specified index."""
        self.log.info(f'Navigating to tab {idxTab}')
        self.tabControl.select(idxTab)
    
    def onTabSelection(self, event: tk.Event):
        """Notebook widget tab selection event."""
        selectedTab = event.widget.select()
        tabText = event.widget.tab(selectedTab, "text")
        self.log.info('Tab selected: %s', tabText)
        oTab: TabModule
        oTab = self.dictTabs[tabText]
        if oTab is None:
            self.log.error('Could not find tab %s', tabText)
        else:
            oTab.loadTab()

    def createWidgets(self):
        """Create user widgets"""
        pass

    def createFrames(self):
        """Create basic frames for the widgets"""
        pass
    
    def displayData(self):
        """Display user data in the widgets"""
        pass

    def setStatus(self, sStatus):
        """Display message in status label"""
        self.log.info('Setting status to %s', sStatus)
        self.lblStatus.configure(text = sStatus)

class TabModule:
    """ A module for the TabsApp. """
    log = logging.getLogger('TabModule')
    
    def __init__(self, oParent: TabsApp, sTitle: str, sClass=None):
        self.sTitle = sTitle
        self.oParent = oParent
        self.isLoaded = False
        self.sClass = sClass
        self.oFrame = oParent.addTab(self)
        self.frmLeft    = None
        self.frmCenter  = None
        self.frmRight   = None

    def getTitle(self) -> str:
        return self.sTitle
    
    def loadData(self):
        pass

    def navigateToObject(self, obj):
        """Select the specified object in this module."""
        pass

    def getDataClass(self) -> str:
        """Returns the class of data handled by this module."""
        return self.sClass
    
    def loadTab(self):
        """Load this tab only if needed. Creates the user widgets."""
        if not self.isLoaded:
            self.log.info('Loading %s', self)
            self.createWidgets()
            self.isLoaded = True
            self.loadData()

    def setLoadingIcon(self, isOver = False):
        """Set the window icon to waiting, or reset it to normal."""
        if isOver:
            self.oParent.window.configure(cursor='')
        else:
            self.oParent.window.configure(cursor='watch')
            self.oParent.window.update()

    def createWidgets(self):
        """Create user widgets"""
        self.lblTest = ttk.Label(master=self.oFrame)
        self.lblTest.pack(fill=tk.X)
        self.lblTest.configure(text = f'Test for {self.sTitle} tab')

    def createLeftRightFrames(self):
        """Create frmLeft and frmRight in this tab."""
        self.frmLeft  = ttk.Frame(master=self.oFrame)
        self.frmRight = ttk.Frame(master=self.oFrame)
        self.frmLeft.pack( fill=tk.Y, side=tk.LEFT, pady=0, padx=6)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=6, padx=6)

    def createLeftCenterRightFrames(self):
        """Create frmLeft, frmCenter and frmRight in this tab."""
        self.frmLeft   = ttk.Frame(master=self.oFrame)
        self.frmCenter = ttk.Frame(master=self.oFrame)
        self.frmRight  = ttk.Frame(master=self.oFrame)
        self.frmLeft.pack(  fill=tk.Y, side=tk.LEFT, pady=0, padx=6)
        self.frmCenter.pack(fill=tk.Y, side=tk.LEFT, pady=5, padx=6)
        self.frmRight.pack( fill=tk.Y, side=tk.LEFT, pady=5, padx=6)

    def enableWidget(self, oWidget, enabled: bool):
        """Enable or disable the widget."""
        if oWidget:
            oWidget['state'] = tk.NORMAL if enabled else tk.DISABLED

    def __str__(self) -> str:
        return f'TabModule {self.sTitle}'

def testTabsApp():
    app = TabsApp('Test')
    modWelcome  = TabModule(app, 'Welcome')
    modSettings = TabModule(app, 'Settings')
    modData     = TabModule(app, 'Data')
    app.setStatus('Welcome to Test of TabsApp')
    app.run()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testTabsApp()
