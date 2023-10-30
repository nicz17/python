"""
Tool to generate HTML pages for the www.tf79.ch website.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import glob
from HtmlPage import *
from GalleryHtmlPage import *

class BuilderTF79:
    log = logging.getLogger('BuilderTF79')
    
    def __init__(self):
        """Constructor"""
        self.log.info('Welcome to build tool for www.tf79.ch !')

    def buildGalleryVoyages(self):
        """Build the index page for gallery/voyages/"""
        self.log.info('Building index for gallery/voyages/')

        aGalleries = []
        aGalleries.append(self.addGalleryLink('Berlin', 'Octobre 2023', 'berlin2023'))
        aGalleries.append(self.addGalleryLink('Boston', 'Juin 2009', 'boston'))

        page = GalleryHtmlPage('Voyages')
        page.addHeading(1, 'Voyages')
        page.addTable(aGalleries, 2, True)
        page.save('index.html')

    def addGalleryLink(self, title, desc, link):
        """Add a galery link"""
        self.log.info('Adding gallery %s', title)
        gal = LinkHtmlTag(link, title)
        return gal


def build():
    """Runs the build methods."""
    builder = BuilderTF79()
    builder.buildGalleryVoyages()

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    build()