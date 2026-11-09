"""
Automatic editor using reflection to find appropriate input widgets.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
from tkinter import ttk
from BaseWidgets import (
    BaseWidget, Button, Label,
    CheckBox, 
    DateTime, DateTimeReadOnly, 
    IntInput, 
    TextReadOnly, TextInput
)


class EditorField:
    """Automatic editor edition field."""
    log = logging.getLogger('EditorField')

    def __init__(self, label: str, mtdGetter, mtdSetter, unit):
        self.label = label
        self.mtdGetter = mtdGetter
        self.mtdSetter = mtdSetter
        self.widLabel = None
        self.widValue = None
        self.unit = unit

    def isReadOnly(self) -> bool:
        return self.mtdSetter is None

    def __str__(self):
        return f'EditorField {self.label} {self.mtdGetter}'

class AutoEditor:
    """Automatic editor."""
    log = logging.getLogger('AutoEditor')
    colorNormal   = 'black'
    colorModified = 'orange'
    colorError    = 'red'
    colorUndef    = 'grey'

    def __init__(self, title: str, objClass, cbkSave=None):
        self.title = title
        self.objClass = objClass
        self.cbkSave = cbkSave
        self.fields = []
        self.object = None

    def addField(self, label: str, mtdGetter, unit=None):
        mtdSetter = None
        name = mtdGetter.__name__
        if name.startswith('get'):
            nameSetter = name.replace('get', 'set')
            self.log.debug(f'Getter {name} class {self.objClass}')
            if callable(getattr(self.objClass, nameSetter, None)):
                mtdSetter = getattr(self.objClass, nameSetter, None)
                self.log.debug(f'Found callable {mtdSetter}')
        self.fields.append(EditorField(label, mtdGetter, mtdSetter, unit))

    def getFields(self) -> list[EditorField]:
        return self.fields

    def loadData(self, obj):
        """Load data from object."""
        self.object = obj
        for field in self.getFields():
            if obj is not None:
                field.widValue.enableWidget(True)
                field.widValue.setValue(obj)
            else:
                field.widValue.setValue(obj)
                field.widValue.enableWidget(False)
        self.enableWidgets()

    def hasChanges(self) -> bool:
        if self.object is None:
            return False
        for field in self.getFields():
            #if field.widValue.isValid() and field.widValue.hasChanges(self.object):
            if field.widValue.hasChanges(self.object):
                return True

    def isValid(self) -> bool:
        """Check if user inputs are valid."""
        for field in self.getFields():
            if not field.widValue.isValid():
                return False
        return True

    def applyLabelColors(self):
        """Set label colors depending on current value."""
        for field in self.getFields():
            color = self.colorNormal
            if self.object is None:
                color = self.colorUndef
            elif not field.widValue.isValid():
                color = self.colorError
            elif field.widValue.hasChanges(self.object):
                color = self.colorModified
            field.widLabel.widget.config(foreground=color)

    def onSave(self, evt=None):
        """Save changes to the edited object."""
        # Apply changes
        for field in self.getFields():
            if not field.isReadOnly():
                if field.widValue.hasChanges(self.object):
                    value = field.widValue.getValue()
                    field.mtdSetter(self.object, value)
        
        # Call save callback
        if self.cbkSave:
            self.cbkSave(self.object)

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.object)

    def onDelete(self):
        """Delete the edited object."""
        pass

    def onModified(self, event=None):
        """Object modification callback."""
        self.enableWidgets()

    def createWidgets(self, parent: ttk.Frame):
        self.frmMain = ttk.LabelFrame(parent, text=self.title)
        self.frmMain.pack()

        self.frmFields = ttk.Frame(self.frmMain)
        self.frmFields.grid(row=0, column=0, padx=4, pady=4, sticky='we')

        for row, field in enumerate(self.getFields()):
            field.widLabel = Label(self.frmFields, field.label)
            field.widLabel.widget.grid(row=row, column=0, sticky='w', padx=0)
            #field.widValue = Label(self.frmFields, None)
            #field.widValue.widget.grid(row=row, column=1, sticky='we', padx=4)
            field.widValue = self.getWidget(field)
            field.widValue.createWidgets(self.frmFields, row, 1)

        self.frmButtons = ttk.Frame(self.frmMain)
        self.frmButtons.grid(row=1, column=0, padx=4, pady=4)
        self.btnSave = Button(self.frmButtons, 'Sauver', self.onSave, 'filesave')
        self.btnSave.grid(0, 0)
        self.btnCancel = Button(self.frmButtons, 'Annuler', self.onCancel, 'cancel')
        self.btnCancel.grid(0, 1)
        self.btnDelete = Button(self.frmButtons, 'Effacer', self.onDelete, 'delete')
        self.btnDelete.grid(0, 2)
        self.enableWidgets()

    def getWidget(self, field: EditorField) -> BaseWidget:
        """Find the edition widget to use for the field."""
        name = field.mtdGetter.__name__
        type = field.mtdGetter.__annotations__["return"]
        self.log.info(f'Getting widget for {field} {name} {type}')
        if type == str:
            if field.isReadOnly():
                return TextReadOnly(field.label, field.mtdGetter)
            else:
                return TextInput(self.onModified, field.mtdGetter, 32)
        elif type == bool:
            return CheckBox(self.onModified, field.mtdGetter, field.label)
        elif type == int:
            return IntInput(self.onModified, field.mtdGetter, field.unit)
        elif type == float:
            if field.isReadOnly():
                return DateTimeReadOnly(field.label, field.mtdGetter)
            else:
                return DateTime(self.onModified, field.mtdGetter)
        else:
            self.log.error(f'Unhandled return type {type} for {field}')
        return None

    def enableWidgets(self):
        editing = self.object is not None
        modified = editing and self.hasChanges()
        valid = editing and self.isValid()

        for field in self.getFields():
            field.widValue.enableWidget(editing)

        self.btnSave.enableWidget(modified and valid)
        self.btnCancel.enableWidget(modified)
        self.btnDelete.enableWidget(False)
        self.applyLabelColors()
