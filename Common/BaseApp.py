"""
 Base app window using Tkinter.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
import sys


class BaseApp:
    log = logging.getLogger('BaseApp')

    def __init__(self, sTitle, sGeometry = '1200x800', sIconFile = None) -> None:
        self.log.info('Creating BaseApp %s [%s]', sTitle, sGeometry)
        self.sTitle = sTitle
        self.window = tk.Tk(className=sTitle)
        self.window.title(sTitle)
        self.window.geometry(sGeometry)

        # Set the application icon if defined
        if sIconFile and os.path.exists(sIconFile):
            self.window.iconphoto(False, tk.PhotoImage(file=sIconFile)) 

        self.createFrames()
        self.createBaseWidgets()
        self.createWidgets()
        self.createBaseButtons()
        self.displayData()

    def run(self):
        self.window.mainloop()
        self.log.info('Goodbye!')

    def createWidgets(self):
        """Create user widgets"""
        pass

    def createBaseWidgets(self):
        """Create base widgets: status label."""
        self.lblStatus = ttk.Label(master=self.frmBottom)
        self.lblStatus.pack(fill=tk.X, side=tk.LEFT) 

    def createBaseButtons(self):
        """Create base buttons: About, Exit."""
        self.btnAbout = self.addButton('About', self.showAboutMsg)
        self.btnExit  = self.addButton('Exit',  self.close)

    def createFrames(self):
        """Create basic frames for the widgets"""
        self.frmTop = ttk.Frame(master=self.window, width=1200, height=100)
        self.frmTop.pack(fill=tk.BOTH, side=tk.TOP)
        self.frmBottom = ttk.Frame(master=self.window, width=1200, height=50)
        self.frmBottom.pack(fill=tk.X, side=tk.BOTTOM)

        self.frmButtons = ttk.Frame(master=self.frmTop, width=100, height=100)
        self.frmButtons.pack(fill=tk.Y, side=tk.LEFT)
        self.frmMain = ttk.Frame(master=self.frmTop, width=700)
        self.frmMain.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def addButton(self, sLabel: str, fnCmd) -> ttk.Button:
        """Add a button with the specified label and callback."""
        btn = ttk.Button(master=self.frmButtons, text=sLabel, command=fnCmd)
        btn.pack(fill=tk.X, padx=4, pady=2)
        return btn

    def displayData(self):
        """Display user data in the widgets"""
        self.setStatus('Welcome to ' + self.sTitle)

    def setStatus(self, sStatus):
        """Display message in status label"""
        self.log.info('Setting status to %s', sStatus)
        self.lblStatus.configure(text = sStatus)

    def onBeforeClose(self):
        """Any last wishes?"""
        pass

    def close(self):
        """Destroy the base window"""
        self.onBeforeClose()
        self.window.destroy()

    def showAboutMsg(self):
        """Display a tk info message about this app."""
        sMsg  = f'{self.sTitle} by {__author__}\n'
        sMsg += f'Version {__version__}\n\n{__copyright__}\n\n'
        sMsg += f'Python {sys.version}\nTkinter {tk.TkVersion}'
        messagebox.showinfo(title='About', message=sMsg)

    def showInfoMsg(self, msg: str):
        """Display a tk info message box."""
        messagebox.showinfo(self.sTitle, msg)

    def showErrorMsg(self, msg: str):
        """Display a tk error message box."""
        messagebox.showerror('Error', msg)
        
    def enableButton(self, btn: ttk.Button, bEnabled: bool):
        """Enable the specified button if bEnabled is true."""
        if btn:
            if bEnabled:
                btn['state'] = tk.NORMAL
            else:
                btn['state'] = tk.DISABLED
