"""
 Pynorpa App window based on TabsApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024"
__version__ = "1.0.0"

import config
import logging
from TabsApp import *
from ModuleCamera import *
import moduleLocations
import moduleSelection
import moduleReselection
import modulePictures
import moduleTaxon
import moduleExpeditions
import modulePublish
import moduleBooks
import moduleBackups
import moduleCalendar
from ttkthemes import ThemedStyle

class PynorpaApp(TabsApp):
    """Pynorpa App window."""
    log = logging.getLogger('PynorpaApp')

    def __init__(self) -> None:
        """Constructor."""
        self.iHeight = 1000
        self.iWidth  = 1600
        sGeometry = f'{self.iWidth}x{self.iHeight}'
        super().__init__('Pynorpa App', sGeometry, config.appIcon)

        # Setting Theme
        style = ThemedStyle(self.window)
        #style.set_theme("scidgrey")
        style.set_theme("radiance")  # Ubuntu
        #style.set_theme("equilux")  # Dark theme

        # Tabbed modules
        modCamera    = ModuleCamera(self)
        modSelection = moduleSelection.ModuleSelection(self)
        modReselect  = moduleReselection.ModuleReselection(self)
        modLocations = moduleLocations.ModuleLocations(self)
        modTaxon     = moduleTaxon.ModuleTaxon(self)
        modPictures  = modulePictures.ModulePictures(self)
        modCalendar  = moduleCalendar.ModuleCalendar(self)
        modExcursion = moduleExpeditions.ModuleExpeditions(self)
        modPublish   = modulePublish.ModulePublish(self)
        modBooks     = moduleBooks.ModuleBooks(self)  # Book design  
        modBackups   = moduleBackups.ModuleBackups(self)

        self.setStatus('Welcome to Pynorpa')