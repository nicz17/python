"""
Tool to generate HTML pages for the www.tf79.ch website.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
from HtmlPage import *
from GalleryHtmlPage import *

class BuilderTF79:
    log = logging.getLogger('BuilderTF79')
    dir = '/home/nicz/www/gallery/'
    
    def __init__(self):
        """Constructor"""
        self.log.info('Welcome to build tool for www.tf79.ch !')

    def buildGalleryVoyages(self):
        """Build the index page for gallery/voyages/"""
        self.log.info('Building index for gallery/voyages/')

        aGalleries = []
        aGalleries.append(self.addGalleryLink('Berlin', 'Octobre 2023', 'berlin2023'))
        aGalleries.append(self.addGalleryLink('Connemara', 'Septembre 2019', 'connemara'))
        aGalleries.append(self.addGalleryLink('Boston et Cape Cod', 'Juin 2012', 'boston'))
        aGalleries.append(self.addGalleryLink('Grèce', 'Juillet 2011', 'grece'))
        aGalleries.append(self.addGalleryLink('Londres', 'Avril 2011', 'london'))
        aGalleries.append(self.addGalleryLink('Berlin', 'Juin 2009', 'berlin'))
        aGalleries.append(self.addGalleryLink('Burundi', 'Juillet 2008', 'burundi'))
        aGalleries.append(self.addGalleryLink('Japon', '2006 et 2007', '../nihon'))
        aGalleries.append(self.addGalleryLink('Suède', 'Juin 2006', 'suede'))
        aGalleries.append(self.addGalleryLink('Madrid', 'Mars 2006', 'madrid'))
        aGalleries.append(self.addGalleryLink('Toledo', 'Mars 2006', 'toledo'))
        aGalleries.append(self.addGalleryLink('Prague', 'Août 2005', 'praha'))
        aGalleries.append(self.addGalleryLink('Budapest', 'Juillet 2005', 'budapest'))
        aGalleries.append(self.addGalleryLink('Ukraine', 'Juillet 2005', '../gbeu/ukraina'))
        aGalleries.append(self.addGalleryLink('Taizé', 'Mai 2005', 'taize'))
        aGalleries.append(self.addGalleryLink('Irlande', 'Mars 2005', 'ireland'))
        aGalleries.append(self.addGalleryLink('Vienne', 'Février 2005', 'vienne'))
        aGalleries.append(self.addGalleryLink('Hawaii', 'Octobre 2003', 'hawaii'))

        page = GalleryHtmlPage('Voyages')
        page.addHeading(1, 'Photos de voyages')
        page.addTable(aGalleries, 2, True).addAttr('width', '100%').addAttr('cellpadding', '20px')
        page.save(f'{self.dir}voyages/index.html')

    def addGalleryLink(self, title, desc, link):
        """Add a gallery link"""
        self.log.info('Adding gallery %s', title)
        pic = os.path.basename(link)
        gal = LinkHtmlTag(f'{link}/index.html', None)
        #gal.addTag(ImageHtmlTag(f'http://www.tf79.ch/gallery/vitrine/{pic}.jpg', title, title))
        gal.addTag(ImageHtmlTag(f'../vitrine/{pic}.jpg', title, title))
        gal.addTag(InlineHtmlTag(f'<br>{title}<br><font color="gray">{desc}</font>', [], None))
        return gal


def build():
    """Runs the build methods."""
    builder = BuilderTF79()
    builder.buildGalleryVoyages()

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    build()