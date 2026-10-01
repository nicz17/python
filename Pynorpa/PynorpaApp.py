"""
 Pynorpa App window based on TabsApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024"
__version__ = "1.0.3"

import logging
from ttkthemes import ThemedStyle

import config
import DateTools
from appParam import AppParamCache
from TabsApp import *

from moduleBackups import ModuleBackups
from moduleBooks import ModuleBooks
from moduleCalendar import ModuleCalendar
from ModuleCamera import ModuleCamera
from moduleExpeditions import ModuleExpeditions
from moduleLocations import ModuleLocations
from modulePictures import ModulePictures
from modulePublish import ModulePublish
from moduleQuality import ModuleQuality
from moduleReselection import ModuleReselection
from moduleSelection import ModuleSelection
from moduleTaxon import ModuleTaxon
from moduleTracking import ModuleTracking


class PynorpaApp(TabsApp):
    """Pynorpa App window."""
    log = logging.getLogger('PynorpaApp')

    def __init__(self) -> None:
        """Constructor. Create window and modules."""
        self.iHeight = 1000
        self.iWidth  = 1600
        sGeometry = f'{self.iWidth}x{self.iHeight}'
        super().__init__('Pynorpa App', sGeometry, config.appIcon)

        # Setting Theme
        style = ThemedStyle(self.window)
        style.set_theme("radiance")  # Ubuntu
        #style.set_theme("scidgrey")
        #style.set_theme("equilux")  # Dark theme

        # Tabbed modules
        ModuleCamera(self)
        ModuleSelection(self)
        ModuleReselection(self)
        ModuleLocations(self)
        ModuleTaxon(self)
        ModulePictures(self)
        ModuleCalendar(self)
        ModuleExpeditions(self)
        ModulePublish(self)
        ModuleBooks(self)
        ModuleBackups(self)
        ModuleQuality(self)
        ModuleTracking(self)

        self.setStatus('Bienvenue à Pynorpa !')
        self.loadNotifications()

    def loadNotifications(self):
        """Load notifications about old backup or upload dates."""
        cache = AppParamCache()

        # Last backup older than a month
        apLastBackup = cache.findByName('backupBook')
        daysBackup = DateTools.getDaysSince(apLastBackup.getDateVal())
        if daysBackup > 35:
            self.addNotification(f'Le dernier backup date de {daysBackup} jours', 'warning')
        
        # Last upload more than 2 weeks ago
        daysUpload = DateTools.getDaysSince(cache.getLastUploadAt())
        if daysUpload > 15:
            self.addNotification(f'Le dernier upload date de {daysUpload} jours', 'warning')

        # Imminent DST switch
        timeUntilSwitch = DateTools.timeUntilNextDSTSwitch()
        if timeUntilSwitch and timeUntilSwitch < 10:
            self.addNotification(f"Changement d'heure dans {timeUntilSwitch} jours!", 'warning')

    def getCredits(self) -> str:
        """App-specific credits to display in About dialog."""
        return '\n\nTkinterMapView by Tom Schimansky'

    def getVersion(self) -> str:
        return __version__