"""
A collection of simple Tk widgets.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
import datetime
import DateTools

        
def enableWidget(widget: tk.Widget, enabled: bool):
    """Enable the specified tk widget if enabled is true."""
    if widget:
        widget['state'] = tk.NORMAL if enabled else tk.DISABLED

class BaseWidget():
    """Base superclass for custom input widgets."""
    log = logging.getLogger('BaseWidget')

    def __init__(self, cbkModified, mtdGetter):
        """Constructor with modification callback and value getter method."""
        self.log.info('Constructor')
        self.cbkModified = cbkModified
        self.mtdGetter = mtdGetter
        self.oWidget = None  # the Tk/Ttk widget

    def getObjectValue(self, object):
        """Get the object value using our getter method."""
        value = None
        if object:
            value = self.mtdGetter(object)
        return value

    def getValue(self):
        """Get the current widget value."""
        return None

    def setValue(self, object):
        """Set the widget value from the specified object."""
        pass
    
    def hasChanges(self, object) -> bool:
        """Check if this widget has changes from the specified object."""
        if object:
            value = self.mtdGetter(object)
            return self.getValue() != value
        return False

    def enableWidget(self, enabled: bool):
        """Enable or disable this widget."""
        if self.oWidget:
            self.oWidget['state'] = tk.NORMAL if enabled else tk.DISABLED
    
    def __str__(self) -> str:
        return 'BaseWidget'

    
class IntInput(BaseWidget):
    """An integer input widget based on ttk.Entry."""
    log = logging.getLogger('IntInput')

    def __init__(self, cbkModified, mtdGetter):
        """Constructor with modification callback."""
        super().__init__(cbkModified, mtdGetter)

    def setValue(self, object):
        """Set the integer value."""
        self.oWidget.delete(0, tk.END)
        value = self.getObjectValue(object)
        if value is not None:
            self.oWidget.insert(0, f'{value}')

    def getValue(self) -> int:
        """Get the current integer value."""
        value = None
        sValue = self.oWidget.get().strip()
        if sValue:
            value = int(sValue)
        return value
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        cmdValidate = (parent.register(self.cbkValidate))
        self.oWidget = ttk.Entry(parent, width=8, validate='all', 
                                validatecommand=(cmdValidate, '%P'))
        self.oWidget.grid(row=row, column=col, padx=5, sticky='w')
        if self.cbkModified:
            self.oWidget.bind('<KeyRelease>', self.cbkModified)

    def cbkValidate(self, input: str) -> bool:
        """Check if input is a digit or empty."""
        return str.isdigit(input) or input == ""
    
    def __str__(self) -> str:
        return 'IntInput'

class TextInput(BaseWidget):
    """A single-line text input widget based on ttk.Entry."""
    log = logging.getLogger('TextInput')

    def __init__(self, cbkModified, mtdGetter):
        """Constructor with modification callback."""
        super().__init__(cbkModified, mtdGetter)
        self.nChars = 64

    def setValue(self, object):
        """Set the string value."""
        self.oWidget.delete(0, tk.END)
        value = self.getObjectValue(object)
        if value:
            self.oWidget.insert(0, value)

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oWidget.get().strip()
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oWidget = ttk.Entry(parent, width=self.nChars)
        self.oWidget.grid(row=row, column=col, padx=5, sticky='we')
        if self.cbkModified:
            self.oWidget.bind('<KeyRelease>', self.cbkModified)
    
    def __str__(self) -> str:
        return 'TextInput'
    
class DateTime(TextInput):
    """A text input widget displaying a float value as date and time."""
    log = logging.getLogger('DateTime')

    def __init__(self, cbkModified, mtdGetter):
        """Constructor with modification callback."""
        super().__init__(cbkModified, mtdGetter)
        self.nChars = 20

    def setValue(self, object):
        """Set the string value."""
        self.oWidget.delete(0, tk.END)
        fvalue = self.getObjectValue(object)
        if fvalue:
            if isinstance(fvalue, float):
                self.oWidget.insert(0, DateTools.timestampToString(fvalue))
            elif isinstance(fvalue, datetime.datetime):
                self.oWidget.insert(0, DateTools.datetimeToString(fvalue))
            else:
                self.log.error('Unhandled date type %s', fvalue)
                self.oWidget.insert(0, 'Error')

    def getValue(self) -> str:
        """Get the current timestamp value."""
        svalue = self.oWidget.get().strip()
        return DateTools.stringToTimestamp(svalue)
    
    def hasChanges(self, object) -> bool:
        return False
    
    def __str__(self) -> str:
        return 'DateTime'

class TextArea(BaseWidget):
    """A multi-line text input widget based on tk.Text."""
    log = logging.getLogger('TextArea')

    def __init__(self, name: str, mtdGetter, nLines=6, cbkModified=None):
        """Constructor with modification callback."""
        self.log.info('Constructor for %s', name)
        super().__init__(cbkModified, mtdGetter)
        self.name = name
        self.nLines = nLines

    def setValue(self, object):
        """Set the string value."""
        value = self.getObjectValue(object)
        self.oWidget['state'] = tk.NORMAL
        self.oWidget.delete(1.0, tk.END)
        if value:
            self.oWidget.insert(1.0, value)

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oWidget.get(1.0, tk.END).strip()
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int, width=64):
        """Create widget in parent frame with grid layout."""
        self.oWidget = tk.Text(parent, width=width, height=self.nLines)
        self.oWidget.grid(row=row, column=col, padx=4, sticky='we')
        if self.cbkModified:
            self.oWidget.bind("<<Modified>>", self.cbkModified)

    def resetModified(self):
        """Reset the modified flag."""
        self.oWidget.edit_modified(False)
    
    def __str__(self) -> str:
        return f'TextArea for {self.name}'

class TextReadOnly(BaseWidget):
    """A read-only text widget based on tk.Label."""
    log = logging.getLogger('TextReadOnly')

    def __init__(self, name: str, mtdGetter):
        """Constructor with attribute name."""
        super().__init__(None, mtdGetter)
        self.log.info('Constructor for %s', name)
        self.name = name

    def setValue(self, object):
        """Set the string value."""
        value = self.getObjectValue(object)
        self.oLabel.configure(text = (value if value is not None else ''))

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oLabel.cget('text')
    
    def hasChanges(self, object) -> bool:
        return False
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oLabel = tk.Label(parent)
        self.oLabel.grid(row=row, column=col, padx=5, sticky='w')
    
    def __str__(self) -> str:
        return f'TextReadOnly for {self.name}'
    
class DateTimeReadOnly(TextReadOnly):
    """A read-only label displaying a float value as date and time."""
    log = logging.getLogger('DateTime')

    def __init__(self, name: str, mtdGetter):
        """Constructor with modification callback."""
        super().__init__(name, mtdGetter)

    def setValue(self, object):
        """Set the string value."""
        self.oLabel.configure(text = '')
        fvalue = self.getObjectValue(object)
        if fvalue:
            if isinstance(fvalue, float):
                self.oLabel.configure(text = DateTools.timestampToString(fvalue))
            elif isinstance(fvalue, datetime.datetime):
                self.oLabel.configure(text = DateTools.datetimeToString(fvalue))
            else:
                self.log.error('Unhandled date type %s', fvalue)
                self.oLabel.configure(text = 'Error')
    
    def __str__(self) -> str:
        return f'DateTimeReadOnly for {self.name}'

class ComboBox():
    """A multiple-choice widget based on ttk.Combobox."""
    log = logging.getLogger('ComboBox')

    def __init__(self, cbkModified):
        """Constructor with modification callback."""
        self.log.info('Constructor')
        self.cbkModified = cbkModified

    def setValues(self, values):
        """Set the possible values."""
        self.oCombo['values'] = values

    def setValue(self, value: str):
        """Set the string value."""
        if value is not None:
            self.oCombo.set(value)

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oCombo.get()
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oCombo = ttk.Combobox(parent, state='readonly', values=[])
        self.oCombo.grid(row=row, column=col, padx=5, sticky='we')
        if self.cbkModified:
            self.oCombo.bind("<<ComboboxSelected>>", self.cbkModified)

    def enableWidget(self, enabled: bool):
        """Enable or disable this widget."""
        enableWidget(self.oCombo, enabled)
    
    def __str__(self) -> str:
        return 'ComboBox'
    
class CheckBox(BaseWidget):
    """A boolean check-box based on ttk.Checkbutton."""
    log = logging.getLogger('CheckBox')

    def __init__(self, cbkModified, mtdGetter, label = ''):
        """Constructor with modification callback."""
        super().__init__(cbkModified, mtdGetter)
        self.label = label
        self.varValue = tk.BooleanVar(value = False)

    def setValue(self, object):
        """Set the boolean value."""
        value = self.getObjectValue(object)
        if value is None:
            self.varValue.set(False)
        else:
            self.varValue.set(value)
        self.enableWidget(value is not None)

    def getValue(self) -> bool:
        """Get the current boolean value."""
        return self.varValue.get()
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oWidget = ttk.Checkbutton(parent, 
            text = self.label, command = self.cbkModified,
            variable = self.varValue)
        self.oWidget.grid(row=row, column=col, padx=5, sticky='we')

class BaseEditor():
    """Common superclass for edition widgets."""
    log = logging.getLogger('BaseEditor')

    def __init__(self, cbkSave=None):
        """Constructor with save callback."""
        self.log.info('Constructor')
        self.cbkSave = cbkSave
        self.widgets = []
        self.row = 0
        self.btnSave = None
        self.btnCancel = None
        self.btnDelete = None

    def setValue(self, object):
        """Set each widget value from the specified object."""
        self.enableWidgets()
        oWidget: BaseWidget
        for oWidget in self.widgets:
            oWidget.setValue(object)
        self.enableWidgets()

    def hasChanges(self, object) -> bool:
        """Check if this editor has changes compared to the specified object."""
        oWidget: BaseWidget
        for oWidget in self.widgets:
            if oWidget.hasChanges(object):
                return True
        return False

    def onModified(self, evt = None):
        """Callback for widget modifications."""
        #self.log.info('BaseEditor modified cbk')
        self.enableWidgets()

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        pass

    def onCancel(self):
        """Cancel changes to the edited object."""
        pass

    def onDelete(self):
        """Delete the edited object."""
        pass

    def createWidgets(self, parent: tk.Frame, title: str):
        """Add the editor widgets to the parent widget."""
        self.frmEdit = ttk.LabelFrame(parent, text=title)
        self.frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=False, pady=5)

    def createButtons(self, bSave: bool, bCancel: bool, bDelete: bool):
        """Add save, cancel and delete buttons."""
        frmButtons = ttk.Frame(self.frmEdit, padding=5)
        frmButtons.grid(row=self.row, column=0, columnspan=2)
        if bSave:
            self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
            self.btnSave.grid(row=0, column=0, padx=3)
        if bCancel:
            self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
            self.btnCancel.grid(row=0, column=1, padx=3)
        if bDelete:
            self.btnDelete = tk.Button(frmButtons, text = 'Delete', command = self.onDelete)
            self.btnDelete.grid(row=0, column=2, padx=3)

    def addText(self, label: str, mtdGetter) -> TextInput:
        """Add a single-line text input."""
        self.addLabel(label)
        oInput = TextInput(self.onModified, mtdGetter)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput)
        return oInput
    
    def addTextArea(self, label: str, mtdGetter, nLines=6, width=64) -> TextArea:
        """Add a multi-line text input."""
        self.addLabel(label)
        oInput = TextArea(label, mtdGetter, nLines, self.onModified)
        oInput.createWidgets(self.frmEdit, self.row, 1, width)
        self.addWidget(oInput)
        return oInput
    
    def addTextReadOnly(self, label: str, mtdGetter) -> TextReadOnly:
        """Add a read-only text."""
        self.addLabel(label)
        oInput = TextReadOnly(label, mtdGetter)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput)
        return oInput
    
    def addIntInput(self, label: str, mtdGetter) -> IntInput:
        """Add an integer input."""
        self.addLabel(label)
        oInput = IntInput(self.onModified, mtdGetter)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput)
        return oInput
    
    def addComboBox(self, label: str, values) -> ComboBox:
        """Add a combo box."""
        self.addLabel(label)
        oCombo = ComboBox(self.onModified)
        oCombo.createWidgets(self.frmEdit, self.row, 1)
        oCombo.setValues(values)
        self.row += 1
        return oCombo
    
    def addCheckBox(self, label: str, mtdGetter, text = '') -> CheckBox:
        """Add a check box."""
        self.addLabel(label)
        oCheckBox = CheckBox(self.onModified, mtdGetter, text)
        oCheckBox.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oCheckBox)
        return oCheckBox

    def addDateTime(self, label: str, mtdGetter) -> DateTime:
        """Add a single-line date-time input."""
        self.addLabel(label)
        oInput = DateTime(self.onModified, mtdGetter)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput)
        return oInput
    
    def addDateTimeReadOnly(self, label: str, mtdGetter) -> TextReadOnly:
        """Add a read-only text."""
        self.addLabel(label)
        oInput = DateTimeReadOnly(label, mtdGetter)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput)
        return oInput

    def addLabel(self, label: str):
        """Add an attribute label at the specified row."""
        oLabel = tk.Label(self.frmEdit, text=label)
        oLabel.grid(row=self.row, column=0, sticky='nw')

    def addWidget(self, oWidget: BaseWidget):
        """Add a widget and bump the row count."""
        self.widgets.append(oWidget)
        self.row += 1

    def enableWidgets(self, enabled = False):
        """Enable our internal widgets."""
        oWidget: BaseWidget
        for oWidget in self.widgets:
            oWidget.enableWidget(enabled)

    def __str__(self) -> str:
        return 'BaseEditor'
