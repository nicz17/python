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
        # The return value of the dialog.
        self.log.info('Open modal dialog window with title %s', title)
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
        self.btnExit = tk.Button(self.root, text='Exit', command=self.exit)
        self.btnExit.pack()

    def exit(self):
        """Close the modal window. Release event grab."""
        self.log.info('Close modal dialog window')
        #self.data = self.entry.get()
        self.root.grab_release()
        self.root.destroy()