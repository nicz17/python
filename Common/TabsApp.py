"""
 Subclass of BaseApp using tabbed frames.
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

    def __init__(self, sTitle, sGeometry = '1200x800') -> None:
        super().__init__(sTitle, sGeometry)

    def createBaseWidgets(self):
        """Create base widgets"""
        self.frmTop = tk.Frame(master=self.window, width=1200, height=800)
        self.frmTop.pack(fill=tk.X, side=tk.TOP)
        self.frmButtons = tk.Frame(master=self.frmTop, width=100, height=800)
        self.frmButtons.pack(fill=tk.Y, side=tk.LEFT)
        self.frmBottom = tk.Frame(master=self.window, width=1200, height=50, bg='red')
        self.frmBottom.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.tabControl = ttk.Notebook(self.frmTop)
        self.tabControl.pack(expand=1, fill="both", pady=3)

        self.lblStatus = tk.Label(master=self.frmBottom)
        self.lblStatus.pack(fill=tk.X) 
        
    def addTab(self, sName):
        self.log.info('Adding tab %s', sName)
        tab = ttk.Frame(self.tabControl)
        self.tabControl.add(tab, text = sName)
        return tab

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
    
    def __init__(self, oParent: TabsApp, sTitle: str):
        self.sTitle = sTitle
        self.oParent = oParent
        self.oFrame = oParent.addTab(sTitle)
        self.createWidgets()

    def createWidgets(self):
        """Create user widgets"""
        self.lblTest = tk.Label(master=self.oFrame)
        self.lblTest.pack(fill=tk.X)
        self.lblTest.configure(text = f'Test for {self.sTitle} tab')

def testTabsApp():
    app = TabsApp('Test')
    modWelcome  = TabModule(app, 'Welcome')
    modSettings = TabModule(app, 'Settings')
    modData     = TabModule(app, 'Data')
    app.setStatus('Welcome to Test of TabsApp')
    app.run()

if __name__ == '__main__':
    testTabsApp()
