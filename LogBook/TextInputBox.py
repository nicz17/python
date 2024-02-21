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
        return self.txtInput.get(1.0, tk.END).strip()
    
    def onReturnKey(self, evt = None):
        """Callback for text widget Return key press."""
        content = self.getContent()
        if content and len(content) > 0:
            self.cbkAdd(content)

    def build(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""

        # Compute optimal width
        #self.log.info('Parent width is %d', parent.winfo_width())
        widthTxt = int((parent.winfo_width() - 140.8)/5.4) + 1
        #self.log.info('text width is %d', widthTxt)

        # Add input TextBox
        self.txtInput = tk.Text(parent, height=1, width=10) 
        self.txtInput.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.txtInput.bind("<<Modified>>", self.enableWidgets)
        self.txtInput.bind("<Return>", self.onReturnKey)
        
        # Add button
        #icon = tk.PhotoImage(file = '/home/nicz/prog/icons/add.png') 
        #self.btnAdd = tk.Button(parent, image=icon, command = self.cbkAdd)
        #self.btnAdd.image = icon
        self.btnAdd = tk.Button(parent, text = 'Add', command = self.onReturnKey)
        self.btnAdd.pack(side=tk.LEFT, padx=3)

        self.enableWidgets()

    def enableWidgets(self, event = None):
        """Enable or disable widgets based on current state."""
        #self.log.info('Enable for content %s', self.getContent())
        enabled = (len(self.getContent()) > 0)
        if enabled:
            self.btnAdd['state'] = tk.NORMAL
        else:
            self.btnAdd['state'] = tk.DISABLED
        self.txtInput.edit_modified(False)

    def clear(self):
        """Clear the text input content."""
        self.txtInput.delete(1.0, tk.END)