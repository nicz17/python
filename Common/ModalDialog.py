"""
Tkinter modal dialog window.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging

class ModalDialog(object):
    log = logging.getLogger(__name__)

    def __init__(self, parent, title=None):
        self.log.info('Open modal dialog window with title %s', title)

        # The return value of the dialog.
        self.data = None

        self.root = tk.Toplevel(parent)
        if title is not None:
            self.root.title(title)
        self.root.geometry('600x400')
        self.createWidgets()

        # Modal window.
        # Wait for visibility or grab_set doesn't seem to work.
        self.root.wait_visibility()
        self.root.grab_set()
        self.root.transient(parent)
        self.parent = parent

        self.loadData()

    def loadData(self):
        """Load user data."""
        pass

    def getData(self):
        """Returns the user input value of this dialog."""
        return self.data

    def setLoadingIcon(self, isLoading=True):
        """Set the window icon to waiting, or reset it to normal."""
        if isLoading:
            self.root.configure(cursor='watch')
            self.root.update()
        else:
            self.root.configure(cursor='')

    def createWidgets(self):
        """Create the user widgets."""
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.btnExit = tk.Button(self.root, text='OK', command=self.accept)
        self.btnExit.pack()
        self.btnCancel = tk.Button(self.root, text='Cancel', command=self.cancel)
        self.btnCancel.pack()

    def accept(self):
        """Accept user input and close."""
        self.data = self.entry.get()
        self.exit()

    def cancel(self):
        """Close dialog and set data to None."""
        self.data = None
        self.exit()

    def exit(self):
        """Close the modal window. Release event grab."""
        self.log.info('Close modal dialog window')
        self.root.grab_release()
        self.root.destroy()