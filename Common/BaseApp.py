"""
 Base app window using Tkinter.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging

class BaseApp:
    log = logging.getLogger('BaseApp')

    def __init__(self, sTitle, sGeometry = '1200x800') -> None:
        self.log.info('Creating BaseApp %s [%s]', sTitle, sGeometry)
        self.sTitle = sTitle
        self.window = tk.Tk()
        self.window.title(sTitle)
        self.window.geometry(sGeometry)
        self.createFrames()
        self.createBaseWidgets()
        self.createWidgets()
        self.displayData()

    def run(self):
        self.window.mainloop()
        self.log.info('Goodbye!')

    def createWidgets(self):
        """Create user widgets"""
        pass

    def createBaseWidgets(self):
        """Create base widgets"""

        btnExit = tk.Button(master=self.frmButtons, text='Exit', command=self.close)
        btnExit.pack(fill=tk.X, padx=4, pady=2)

        self.lblStatus = tk.Label(master=self.frmBottom)
        self.lblStatus.pack(fill=tk.X) 

    def createFrames(self):
        """Create basic frames for the widgets"""
        self.frmTop = tk.Frame(master=self.window, width=1200, height=100)
        self.frmTop.pack(fill=tk.X, side=tk.TOP)
        self.frmBottom = tk.Frame(master=self.window, width=1200, height=50, bg='red')
        self.frmBottom.pack(fill=tk.X, side=tk.BOTTOM)

        self.frmButtons = tk.Frame(master=self.frmTop, width=100, height=100)
        self.frmButtons.pack(fill=tk.Y, side=tk.LEFT)
        self.frmMain = tk.Frame(master=self.frmTop, width=700)
        self.frmMain.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def displayData(self):
        """Display user data in the widgets"""
        self.setStatus('Welcome to ' + self.sTitle)

    def setStatus(self, sStatus):
        """Display message in status label"""
        self.log.info('Setting status to %s', sStatus)
        self.lblStatus.configure(text = sStatus)

    def close(self):
        """Destroy the base window"""
        self.window.destroy()
