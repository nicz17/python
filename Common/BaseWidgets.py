"""
A collection of simple Tk widgets.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk

        
def enableWidget(widget: tk.Widget, enabled: bool):
    """Enable the specified tk widget if enabled is true."""
    if widget:
        widget['state'] = tk.NORMAL if enabled else tk.DISABLED

class IntInput():
    """A integer input widget based on ttk.Entry."""
    log = logging.getLogger('IntInput')

    def __init__(self, cbkModified):
        """Constructor with modification callback."""
        self.log.info('Constructor')
        self.cbkModified = cbkModified

    def setValue(self, value: int):
        """Set the integer value."""
        self.oEntry.delete(0, tk.END)
        if value is not None:
            self.oEntry.insert(0, f'{value}')

    def getValue(self) -> int:
        """Get the current integer value."""
        value = None
        sValue = self.oEntry.get().strip()
        if sValue:
            value = int(sValue)
        return value
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        cmdValidate = (parent.register(self.cbkValidate))
        self.oEntry = ttk.Entry(parent, width=8, validate='all', 
                                validatecommand=(cmdValidate, '%P'))
        self.oEntry.grid(row=row, column=col, padx=5, sticky='w')
        if self.cbkModified:
            self.oEntry.bind('<KeyRelease>', self.cbkModified)

    def enableWidget(self, enabled: bool):
        """Enable or disable this widget."""
        enableWidget(self.oEntry, enabled)

    def cbkValidate(self, input: str) -> bool:
        """Check if input is a digit or empty."""
        return str.isdigit(input) or input == ""
    
    def __str__(self) -> str:
        return 'IntInput'

class TextInput():
    """A single-line text input widget based on ttk.Entry."""
    log = logging.getLogger('TextInput')

    def __init__(self, cbkModified):
        """Constructor with modification callback."""
        self.log.info('Constructor')
        self.cbkModified = cbkModified

    def setValue(self, value: str):
        """Set the string value."""
        self.oEntry.delete(0, tk.END)
        if value:
            self.oEntry.insert(0, value)

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oEntry.get().strip()
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oEntry = ttk.Entry(parent, width=64)
        self.oEntry.grid(row=row, column=col, padx=5, sticky='we')
        if self.cbkModified:
            self.oEntry.bind('<KeyRelease>', self.cbkModified)

    def enableWidget(self, enabled: bool):
        """Enable or disable this widget."""
        enableWidget(self.oEntry, enabled)
    
    def __str__(self) -> str:
        return 'TextInput'

class TextArea():
    """A multi-line text input widget based on tk.Text."""
    log = logging.getLogger('TextArea')

    def __init__(self, name: str, nLines=6, cbkModified=None):
        """Constructor with modification callback."""
        self.log.info('Constructor for %s', name)
        self.name = name
        self.nLines = nLines
        self.cbkModified = cbkModified

    def setValue(self, value: str):
        """Set the string value."""
        self.oText.delete(1.0, tk.END)
        if value:
            self.oText.insert(1.0, value)

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oText.get(1.0, tk.END).strip()
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oText = tk.Text(parent, width=64, height=self.nLines)
        self.oText.grid(row=row, column=col, padx=4, sticky='we')
        if self.cbkModified:
            self.oText.bind("<<Modified>>", self.cbkModified)

    def enableWidget(self, enabled: bool):
        """Enable or disable this widget."""
        enableWidget(self.oText, enabled)

    def resetModified(self):
        """Reset the modified flag."""
        self.oText.edit_modified(False)
    
    def __str__(self) -> str:
        return f'TextArea for {self.name}'

class TextReadOnly():
    """A read-only text widget based on tk.Label."""
    log = logging.getLogger('TextReadOnly')

    def __init__(self, name: str):
        """Constructor with attribute name."""
        self.log.info('Constructor for %s', name)
        self.name = name

    def setValue(self, value: str):
        """Set the string value."""
        self.oLabel.configure(text = (value if value is not None else ''))

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oLabel.cget('text')
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oLabel = tk.Label(parent)
        self.oLabel.grid(row=row, column=col, padx=5, sticky='w')
    
    def __str__(self) -> str:
        return f'TextReadOnly for {self.name}'


class BaseEditor():
    """Common superclass for edition widgets."""
    log = logging.getLogger('BaseEditor')

    def __init__(self, cbkSave=None):
        """Constructor with save callback."""
        self.log.info('Constructor')
        self.cbkSave = cbkSave
        self.row = 0

    def onModified(self, evt=None):
        """Callback for widget modifications."""
        #self.log.info('BaseEditor modified cbk')
        self.enableWidgets()

    def createWidgets(self, parent: tk.Frame, title: str):
        """Add the editor widgets to the parent widget."""
        self.frmEdit = ttk.LabelFrame(parent, text=title)
        self.frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

    def addText(self, label: str) -> TextInput:
        """Add a single-line text input."""
        self.addLabel(label)
        oInput = TextInput(self.onModified)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput
    
    def addTextArea(self, label: str, nLines: int) -> TextArea:
        """Add a multi-line text input."""
        self.addLabel(label)
        oInput = TextArea(label, nLines, self.onModified)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput
    
    def addTextReadOnly(self, label: str) -> TextReadOnly:
        """Add a read-only text."""
        self.addLabel(label)
        oInput = TextReadOnly(label)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput
    
    def addIntInput(self, label: str) -> IntInput:
        """Add an integer input."""
        self.addLabel(label)
        oInput = IntInput(self.onModified)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput

    def addLabel(self, label: str):
        """Add an attribute label at the specified row."""
        oLabel = tk.Label(self.frmEdit, text=label)
        oLabel.grid(row=self.row, column=0, sticky='nw')

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        pass
        
    # def enableWidget(self, widget: tk.Widget, enabled: bool):
    #     """Enable the specified tk widget if enabled is true."""
    #     if widget:
    #         widget['state'] = tk.NORMAL if enabled else tk.DISABLED

    def __str__(self) -> str:
        return 'BaseEditor'
