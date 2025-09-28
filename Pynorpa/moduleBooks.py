"""
Pynorpa module to help create photo albums or calendars 
with iFolor or smartphoto.ch
"""

# TODO add Books module 
# - Book has name, description, status, list of pictures
# - status: Project, Ongoing, Ordered, Done
# - select Pictures by filtering on Location or Taxon
# - find original file on disk or backups by matching timestamp
# - add original image file to Book directory orig/ for edition
# - save Book contents in json file
# - generate Book preview html file with medium images and comments 

import config
import logging

from TabsApp import TabModule, TabsApp


class ModuleBooks(TabModule):
    """Class to help design books."""
    log = logging.getLogger('ModuleBooks')

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        super().__init__(parent, 'Livres')
        self.book = None