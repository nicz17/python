"""
 Pynorpa App window based on TabsApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from TabsApp import *
from ModuleCamera import *
import moduleLocations
import moduleSelection
import modulePictures
import moduleTaxon
from ttkthemes import ThemedStyle

class PynorpaApp(TabsApp):
    """Pynorpa App window."""
    log = logging.getLogger('PynorpaApp')

    def __init__(self) -> None:
        """Constructor."""
        self.iHeight = 1000
        self.iWidth  = 1500
        sGeometry = f'{self.iWidth}x{self.iHeight}'
        super().__init__('Pynorpa App', sGeometry)

        # Setting Theme
        style = ThemedStyle(self.window)
        #style.set_theme("scidgrey")
        style.set_theme("radiance")  # Ubuntu
        #style.set_theme("equilux")  # Dark theme

        modCamera    = ModuleCamera(self)
        modSelection = moduleSelection.ModuleSelection(self)
        modLocations = moduleLocations.ModuleLocations(self)
        modTaxon     = moduleTaxon.ModuleTaxon(self)
        modPictures  = modulePictures.ModulePictures(self)

        self.setStatus('Welcome to Pynorpa')