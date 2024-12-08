"""Module TaxonUrlProvider"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from taxon import TaxonRank, Taxon
from HtmlPage import LinkHtmlTag

class TaxonUrlProvider():
    """Class TaxonUrlProvider"""
    log = logging.getLogger("TaxonUrlProvider")

    def __init__(self, text: str, baseUrl: str, tooltip: str, filterRank=None, filterNames=None, formatter=None):
        """Constructor with site name, URL, and optional filters."""
        self.text = text
        self.baseUrl = baseUrl
        self.tooltip = tooltip
        self.filterRank = filterRank
        self.filterNames = ([] if filterNames is None else filterNames)
        self.formatter = formatter

    def getLink(self, taxon: Taxon) -> LinkHtmlTag:
        """Builds the html link to the external site."""
        link = None
        formatted = taxon.getName()
        if self.formatter:
            formatted = self.formatter(taxon)
        if self.applies(taxon):
            link = LinkHtmlTag(f'{self.baseUrl}{formatted}', self.text, True, self.tooltip)
        return link

    def applies(self, taxon: Taxon) -> bool:
        """Check if the URL provider applies to the sepcified taxon."""
        if taxon is None:
            return False
        if self.filterRank is None:
            return True
        ancestor = taxon.getAncestor(self.filterRank)
        if ancestor.getName() in self.filterNames:
            return True
        return False
    
    def formatEmpty(taxon: Taxon):
        return ''
    
    def formatGalerieInsecte(taxon: Taxon):
        return f"{taxon.getName().replace(' ', '_')}.html"
    
    def formatAntWiki(taxon: Taxon):
        return f"{taxon.getName().replace(' ', '_')}"
    
    def formatVogelwarte(taxon: Taxon):
        return f"{taxon.getNameFr().replace(' ', '-').lower()}"
    
    def formatInfoFlora(taxon: Taxon):
        return f"{taxon.getName().replace(' ', '-').lower()}.html"
    
    def formatMycoDb(taxon: Taxon):
        return f"{taxon.getName().replace(' ', '&espece=')}"

    def __str__(self):
        return f'TaxonUrlProvider for {self.text}'


def testTaxonUrlProvider():
    """Unit test for TaxonUrlProvider"""
    TaxonUrlProvider.log.info("Testing TaxonUrlProvider")
    obj = TaxonUrlProvider(None, None, None, None, None, None)
    obj.log.info(obj)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testTaxonUrlProvider()
