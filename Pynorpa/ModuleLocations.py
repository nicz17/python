"""
 Pynorpa Module for displaying and editing locations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

#import tkinter as tk
import logging
from TabsApp import *
from BaseTable import *
from LocationCache import *

class ModuleLocations(TabModule):
    """Pynorpa Module for locations."""
    log = logging.getLogger('ModuleLocations')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.table = BaseTable(self.onSelectLocation)
        super().__init__(parent, 'Lieux')

    def onSelectLocation(self):
        pass

    def createWidgets(self):
        """Create user widgets."""
        columns = ('Nom', 'Région', 'Altitude')
        self.table.createWidgets(self.oFrame, columns)