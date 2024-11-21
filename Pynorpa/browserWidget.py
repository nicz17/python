"""
Tkinterweb browser widget.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import tkinterweb
import logging

class BrowserWidget():
    """A browser widget based on tkinterweb."""
    log = logging.getLogger('BrowserWidget')

    def __init__(self):
        """Constructor"""
        self.web = None

    def loadData(self, filename: str):
        """Load the specified local html file."""
        self.web.load_file(filename, force=True)
        
    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        self.web = tkinterweb.HtmlFrame(parent, messages_enabled=False)
        self.web.pack(fill=tk.BOTH, expand=True)