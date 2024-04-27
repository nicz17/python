"""
 Pynorpa App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from TabsApp import *
from ModuleCamera import *
from ModuleLocations import *

class PynorpaTabsApp(TabsApp):
    """Pynorpa App window."""
    log = logging.getLogger('PynorpaTabsApp')

    def __init__(self) -> None:
        """Constructor."""
        self.iHeight = 800
        self.iWidth  = 1000
        sGeometry = f'{self.iWidth}x{self.iHeight}'
        super().__init__('Pynorpa Tabs', sGeometry)

        modLocations = ModuleLocations(self)
        modCamera    = ModuleCamera(self)
        modPictures  = TabModule(self, 'Photos')