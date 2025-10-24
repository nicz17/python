"""
A collection of simple Tk widgets.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import datetime
import DateTools

        
def enableWidget(widget: tk.Widget, enabled: bool):
    """Enable the specified tk widget if enabled is true."""
    if widget:
        widget['state'] = tk.NORMAL if enabled else tk.DISABLED

class Button():
    """A button with label, optional icon and tooltip."""
    log = logging.getLogger('Button')
    dirIcons = f'{Path.home()}/prog/icons'

    def __init__(self, parent: ttk.Frame, label: str, cmd, iconName=None, tooltip=None):
        self.log.debug('Constructor %s %s', label, iconName)
        self.icon = self.getIcon(iconName)
        if self.icon and label:
            self.log.debug('Button with icon for %s %s', label, iconName)
            self.btn = ttk.Button(parent, text=label, image=self.icon, compound=tk.LEFT, command=cmd)
        elif self.icon:
            self.btn = ttk.Button(parent, image=self.icon, command=cmd)
        else:
            self.btn = ttk.Button(parent, text=label, command=cmd)

        self.tooltip = None
        if tooltip:
            self.tooltip = ToolTip(self.btn, tooltip)

    def pack(self, pady=3, side=tk.LEFT):
        self.btn.pack(side=tk.LEFT, padx=3, pady=pady)

    def grid(self, row: int, col: int):
        self.btn.grid(row=row, column=col, padx=3, sticky='w')

    def getIcon(self, iconName: str) -> tk.PhotoImage:
        if iconName:
            file = f'{self.dirIcons}/{iconName}.png'
            if os.path.exists(file):
                return tk.PhotoImage(file=file)
            else:
                self.log.error('Could not find icon image %s', file)
        return None
    
    def setLabel(self, label: str):
        """Change the button label."""
        self.btn.configure(text=label)
    
    def setIcon(self, iconName: str):
        """Change the button icon."""
        self.icon = self.getIcon(iconName)
        self.btn.configure(image=self.icon)
    
    def enableWidget(self, enabled: bool):
        self.btn['state'] = tk.NORMAL if enabled else tk.DISABLED


class IconButton():
    """A button only displaying an icon."""
    log = logging.getLogger("IconButton")
    dirIcons = f'{Path.home()}/prog/icons'

    def __init__(self, parent, icon: str, tooltip: str, cmd, pady=0):
        """Constructor."""
        self.iconName = icon
        self.iconImg = None
        self.tooltip = tooltip
        self.enabled = True
        self.cmd = cmd
        self.setIcon(icon)
        self.lbl = ttk.Label(parent, image=self.iconImg)
        self.lbl.pack(side=tk.LEFT, pady=pady)
        self.lbl.bind("<Button-1>", self.onClick)
        if tooltip:
            self.tt = ToolTip(self.lbl, tooltip)
    
    def setIcon(self, iconName: str):
        """Change the button icon."""
        file = f'{self.dirIcons}/{iconName}.png'
        if os.path.exists(file):
            self.iconImg = tk.PhotoImage(file=file)
        else:
            self.log.error('Could not find icon image %s', file)

    def setEnabled(self, enabled: bool):
        """Setter for enabled"""
        self.enabled = enabled

    def onClick(self, event=None):
        """On click."""
        self.log.debug(f'Clicked {self}')
        if self.enabled and self.cmd:
            self.cmd()

    def __str__(self):
        return f'IconButton {self.iconName} enabled:{self.enabled}'


class BaseWidget():
    """Base superclass for custom input widgets."""
    log = logging.getLogger('BaseWidget')

    def __init__(self, cbkModified, mtdGetter):
        """Constructor with modification callback and value getter method."""
        self.log.info('Constructor')
        self.cbkModified = cbkModified
        self.mtdGetter = mtdGetter
        self.oWidget = None  # the Tk/Ttk widget
        self.oLabel  = None  # optional Ttk label

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

    def setLabel(self, oLabel: ttk.Label):
        self.oLabel = oLabel

    def setLabelColor(self, color: str):
        if self.oLabel:
            self.oLabel.configure(foreground=color)
    
    def hasChanges(self, object) -> bool:
        """Check if this widget has changes from the specified object."""
        if object:
            value = self.mtdGetter(object)
            return self.getValue() != value
        return False
    
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        pass

    def enableWidget(self, enabled: bool):
        """Enable or disable this widget."""
        if self.oWidget:
            self.oWidget['state'] = tk.NORMAL if enabled else tk.DISABLED
    
    def __str__(self) -> str:
        return 'BaseWidget'

    
class IntInput(BaseWidget):
    """An integer input widget based on ttk.Entry."""
    log = logging.getLogger('IntInput')

    def __init__(self, cbkModified, mtdGetter, unit=None):
        """Constructor with modification callback."""
        super().__init__(cbkModified, mtdGetter)
        self.unit = unit

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
        frmWidget = ttk.Frame(parent)
        self.oWidget = ttk.Entry(frmWidget, width=8, validate='all', 
                                validatecommand=(cmdValidate, '%P'))
        frmWidget.grid(row=row, column=col, padx=5, sticky='w')
        self.oWidget.grid(row=0, column=0, padx=0, sticky='w')
        if self.cbkModified:
            self.oWidget.bind('<KeyRelease>', self.cbkModified)
        if self.unit:
            lblUnit = ttk.Label(frmWidget, text=self.unit)
            lblUnit.grid(row=0, column=1, padx=3, sticky='w')

    def cbkValidate(self, input: str) -> bool:
        """Check if input is a digit or empty."""
        return str.isdigit(input) or input == ""
    
    def __str__(self) -> str:
        return 'IntInput'
    
class SpinBox(BaseWidget):
    """An Integer selector from a range."""
    log = logging.getLogger('SpinBox')

    def __init__(self, cbkModified, mtdGetter, iMin: int, iMax: int):
        """Constructor with modification callback and range."""
        super().__init__(cbkModified, mtdGetter)
        self.iMin = iMin
        self.iMax = iMax

    def setValue(self, object):
        """Set the integer value."""
        self.oWidget.delete(0, tk.END)
        intValue = 0
        if object is not None:
            intValue = self.mtdGetter(object)
            if intValue is None:
                intValue = 0
        self.oWidget.insert(0, str(intValue))

    def getValue(self) -> int:
        """Get the current int value."""
        return int(self.oWidget.get())
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        cmdValidate = (parent.register(self.cbkValidate))
        self.oWidget = tk.Spinbox(parent, from_=self.iMin, to=self.iMax, 
                                  command=self.cbkModified, width=8, validate='all', 
                                    validatecommand=(cmdValidate, '%P'))
        self.oWidget.grid(row=row, column=col, padx=4, sticky='w')
        if self.cbkModified:
            self.oWidget.bind('<KeyRelease>', self.cbkModified)

    def cbkValidate(self, input: str) -> bool:
        """Check if input is a digit or empty."""
        return str.isdigit(input) or input == ''
    
    def __str__(self) -> str:
        return f'SpinBox [{self.iMin}:{self.iMax}]'

class TextInput(BaseWidget):
    """A single-line text input widget based on ttk.Entry."""
    log = logging.getLogger('TextInput')

    def __init__(self, cbkModified, mtdGetter, nChars=64):
        """Constructor with modification callback."""
        super().__init__(cbkModified, mtdGetter)
        self.nChars = nChars

    def setValue(self, object):
        """Set the string value."""
        self.oWidget.delete(0, tk.END)
        value = self.getObjectValue(object)
        if value:
            self.oWidget.insert(0, value)

    def getValue(self) -> str:
        """Get the current string value."""
        value = self.oWidget.get().strip()
        if value == '':
            value = None
        return value
    
    def hasChanges(self, object) -> bool:
        """Check if this widget has changes from the specified object."""
        if object:
            objValue = self.mtdGetter(object)
            widValue = self.getValue()
            if (not objValue) and (not widValue):
                return False
        return super().hasChanges(object)
        
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
        self.oWidget = tk.Text(parent, width=width, height=self.nLines, wrap=tk.WORD)
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
        self.oWidget.configure(text = (value if value is not None else ''))

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oWidget.cget('text')
    
    def hasChanges(self, object) -> bool:
        return False
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oWidget = ttk.Label(parent)
        self.oWidget.grid(row=row, column=col, padx=5, sticky='w')
    
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
        self.oWidget.configure(text = '')
        fvalue = self.getObjectValue(object)
        if fvalue:
            if isinstance(fvalue, float):
                self.oWidget.configure(text = DateTools.timestampToString(fvalue))
            elif isinstance(fvalue, datetime.datetime):
                self.oWidget.configure(text = DateTools.datetimeToString(fvalue))
            else:
                self.log.error('Unhandled date type %s', fvalue)
                self.oWidget.configure(text = 'Error')
    
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
    
    def getSelectionIndex(self) -> int:
        """Get the current selection index, 0-based."""
        return self.oCombo.current()
        
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
    
class ComboBoxRefl(BaseWidget):
    """A multiple-choice widget based on ttk.Combobox."""
    log = logging.getLogger('ComboBoxRefl')

    def __init__(self, cbkModified, mtdGetter):
        """Constructor with modification callback."""
        super().__init__(cbkModified, mtdGetter)

    def setValues(self, values):
        """Set the possible values."""
        self.oCombo['values'] = values

    def setValue(self, object):
        """Set the string value."""
        value = self.getObjectValue(object)
        if value is not None:
            self.oCombo.set(value)

    def getValue(self) -> str:
        """Get the current string value."""
        return self.oCombo.get()
    
    def getSelectionIndex(self) -> int:
        """Get the current selection index, 0-based."""
        return self.oCombo.current()
        
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
        return 'ComboBoxRefl'
    
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

    def __init__(self, cbkSave=None, colorLabelDef='black'):
        """Constructor with save callback."""
        self.log.info('Constructor')
        self.object = None
        self.cbkSave = cbkSave
        self.colorLabelDef = colorLabelDef
        self.widgets = []
        self.row = 0
        self.colButton = 0
        self.btnSave = None
        self.btnCancel = None
        self.btnDelete = None

    def setValue(self, object):
        """Set each widget value from the specified object."""
        self.object = object
        self.enableWidgets()
        oWidget: BaseWidget
        for oWidget in self.widgets:
            oWidget.setValue(object)
        self.enableWidgets()

    def hasChanges(self, object) -> bool:
        """Check if this editor has changes compared to the specified object."""
        oWidget: BaseWidget
        hasChanges = False
        for oWidget in self.widgets:
            if oWidget.hasChanges(object):
                oWidget.setLabelColor('orange')
                hasChanges = True
            else:
                oWidget.setLabelColor(self.colorLabelDef)
        return hasChanges

    def onModified(self, evt = None):
        """Callback for widget modifications."""
        #self.log.info('BaseEditor modified cbk')
        self.enableWidgets()

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        pass

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.setValue(self.object)

    def onDelete(self):
        """Delete the edited object."""
        pass

    def createWidgets(self, parent: tk.Frame, title: str):
        """Add the editor widgets to the parent widget."""
        self.frmEdit = ttk.LabelFrame(parent, text=title)
        self.frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=False, pady=5)

    def createButtons(self, bSave: bool, bCancel: bool, bDelete: bool):
        """Add save, cancel and delete buttons."""
        self.frmButtons = ttk.Frame(self.frmEdit, padding=5)
        self.frmButtons.grid(row=self.row, column=0, columnspan=2)
        if bSave:
            self.btnSave   = self.addButton('Sauver', self.onSave, 'filesave')
        if bCancel:
            self.btnCancel = self.addButton('Annuler', self.onCancel, 'cancel')
        if bDelete:
            self.btnDelete = self.addButton('Effacer', self.onDelete, 'delete')

    def enableButtons(self, bEnableSave: bool, bEnableCancel: bool, bEnableDelete: bool):
        """Enable save, cancel and delete buttons."""
        if self.btnSave: 
            self.btnSave.enableWidget(bEnableSave)
        if self.btnCancel: 
            self.btnCancel.enableWidget(bEnableCancel)
        if self.btnDelete: 
            self.btnDelete.enableWidget(bEnableDelete)

    def addButton(self, label: str, cmd, icon=None) -> Button:
        """Add a button with label, command, and optional icon."""
        btn = Button(self.frmButtons, label, cmd, icon)
        btn.grid(0, self.colButton)
        self.colButton += 1
        return btn

    def addText(self, label: str, mtdGetter, nChars=64) -> TextInput:
        """Add a single-line text input."""
        oLabel = self.addLabel(label)
        oInput = TextInput(self.onModified, mtdGetter, nChars)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput, oLabel)
        return oInput
    
    def addTextArea(self, label: str, mtdGetter, nLines=6, width=64) -> TextArea:
        """Add a multi-line text input."""
        oLabel = self.addLabel(label)
        oInput = TextArea(label, mtdGetter, nLines, self.onModified)
        oInput.createWidgets(self.frmEdit, self.row, 1, width)
        self.addWidget(oInput, oLabel)
        return oInput
    
    def addTextReadOnly(self, label: str, mtdGetter) -> TextReadOnly:
        """Add a read-only text."""
        oLabel = self.addLabel(label)
        oInput = TextReadOnly(label, mtdGetter)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput, oLabel)
        return oInput
    
    def addIntInput(self, label: str, mtdGetter, unit=None) -> IntInput:
        """Add an integer input."""
        oLabel = self.addLabel(label)
        oInput = IntInput(self.onModified, mtdGetter, unit)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput, oLabel)
        return oInput
    
    def addComboBox(self, label: str, values) -> ComboBox:
        """Add a combo box."""
        oLabel = self.addLabel(label)
        oCombo = ComboBox(self.onModified)
        oCombo.createWidgets(self.frmEdit, self.row, 1)
        oCombo.setValues(values)
        self.row += 1
        return oCombo
    
    def addComboBoxRefl(self, label: str, mtdGetter, values) -> ComboBoxRefl:
        """Add a combo box."""
        oLabel = self.addLabel(label)
        oCombo = ComboBoxRefl(self.onModified, mtdGetter)
        oCombo.createWidgets(self.frmEdit, self.row, 1)
        oCombo.setValues(values)
        self.addWidget(oCombo, oLabel)
        return oCombo
    
    def addCheckBox(self, label: str, mtdGetter, text = '') -> CheckBox:
        """Add a check box."""
        oLabel = self.addLabel(label)
        oCheckBox = CheckBox(self.onModified, mtdGetter, text)
        oCheckBox.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oCheckBox, oLabel)
        return oCheckBox

    def addSpinBox(self, label: str, mtdGetter, iMin: int, iMax: int) -> SpinBox:
        """Add a integer range input."""
        oLabel = self.addLabel(label)
        oInput = SpinBox(self.onModified, mtdGetter, iMin, iMax)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput, oLabel)
        return oInput

    def addDateTime(self, label: str, mtdGetter) -> DateTime:
        """Add a single-line date-time input."""
        oLabel = self.addLabel(label)
        oInput = DateTime(self.onModified, mtdGetter)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput, oLabel)
        return oInput
    
    def addDateTimeReadOnly(self, label: str, mtdGetter) -> TextReadOnly:
        """Add a read-only text."""
        oLabel = self.addLabel(label)
        oInput = DateTimeReadOnly(label, mtdGetter)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oInput, oLabel)
        return oInput

    def addCustomWidget(self, label: str, oWidget: BaseWidget):
        """Add a custome edition widget."""
        oLabel = self.addLabel(label, 'w')
        oWidget.createWidgets(self.frmEdit, self.row, 1)
        self.addWidget(oWidget, oLabel)
        return oWidget

    def addLabel(self, label: str, sticky='nw') -> ttk.Label:
        """Add an attribute label at the specified row."""
        oLabel = ttk.Label(self.frmEdit, text=label)
        oLabel.grid(row=self.row, column=0, sticky=sticky)
        return oLabel

    def addWidget(self, oWidget: BaseWidget, oLabel: ttk.Label):
        """Add a widget and bump the row count."""
        self.widgets.append(oWidget)
        oWidget.setLabel(oLabel)
        self.row += 1

    def enableWidgets(self, enabled = False):
        """Enable our internal widgets."""
        oWidget: BaseWidget
        for oWidget in self.widgets:
            oWidget.enableWidget(enabled)

    def __str__(self) -> str:
        return 'BaseEditor'


class SearchBar():
    """An iterative search bar widget."""
    log = logging.getLogger("SearchBar")

    def __init__(self, parent: tk.Frame, width: int, cbkSearch):
        """Constructor."""
        self.cbkSearch = cbkSearch
        self.txtInput = ttk.Entry(parent, width=width)
        self.txtInput.pack(side=tk.LEFT, padx=3, fill=tk.X)
        self.txtInput.bind('<Return>', self.onSearch)
        self.btnClear  = IconButton(parent, 'clear-bar', 'Effacer', self.onClear, 6)
        self.btnSearch = IconButton(parent, 'find', 'Chercher', self.onSearch, 6)

    def onClear(self, event=None):
        self.txtInput.delete(0, tk.END)
        self.txtInput.focus_set()

    def onSearch(self, event=None):
        """Search button callback."""
        input = self.txtInput.get()
        if input and len(input) > 2:
            self.cbkSearch(input)

    def enableWidget(self, enabled: bool):
        """Enable widget."""
        enableWidget(self.txtInput, enabled)
        self.btnSearch.setEnabled(enabled)
        self.btnClear.setEnabled(enabled)

    def __str__(self) -> str:
        return 'SearchBar'


class ToolTip():
    """Create a tooltip for a given widget."""

    def __init__(self, widget: tk.Widget, text='widget info'):
        self.waittime = 500     #milliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffd0", relief='solid', borderwidth=1,
                       wraplength = self.wraplength, foreground='#303030')
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()