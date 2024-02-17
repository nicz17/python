"""
A text input widget using a Tk Text and Button.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk


class TextInputBox():
    """A text input widget using a Tk Text and Button."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkAdd):
        """Constructor with add callback."""
        self.log.info('Constructor')
        self.cbkAdd = cbkAdd

    def getContent(self) -> str:
        """Get the text input content."""
        return self.txtInput.get(1.0, tk.END).rstrip()

    def build(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""

        # Add input TextBox 
        self.txtInput = tk.Text(parent, height = 1, width = 28) 
        self.txtInput.pack(fill=tk.X, side=tk.LEFT) 
        
        # Add button
        self.btnAdd = tk.Button(parent, text = 'Add', command = self.cbkAdd)
        self.btnAdd.pack(side=tk.RIGHT)

    def clear(self):
        """Clear the text input content."""
        self.txtInput.delete(1.0, tk.END)