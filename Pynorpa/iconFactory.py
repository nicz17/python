"""Module IconFactory"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from PIL import Image
from taxon import TaxonRank


class IconFactory():
    """Class IconFactory"""
    log = logging.getLogger("IconFactory")

    def __init__(self, dir: str):
        """Constructor."""
        self.dir = dir

    def generateSquareIcon(self, size: int, color: str, filename: str):
        """Generate a square icon"""
        self.log.info(f'Generating {size}x{size} square icon color {color} name {filename}')
        rgb = self.hexToRGB(color)
        self.log.debug(f'Color as RGB: {rgb}')
        img = Image.new('RGB', (size, size), rgb)
        img.save(f'{self.dir}{filename}', 'PNG')

    def hexToRGB(self, hex: str):
        """Transform a hex color code to a RGB triplet."""
        shex = hex.lstrip('#')
        rgb = tuple(int(shex[i:i+2], 16) for i in (0, 2, 4))
        return rgb

    def __str__(self):
        str = "IconFactory"
        str += f' dir: {self.dir}'
        return str


def testIconFactory():
    """Unit test for IconFactory"""
    IconFactory.log.info("Testing IconFactory")
    fact = IconFactory('resources/')
    fact.generateSquareIcon(16, '#4217f0', 'test.png')
    for rank in TaxonRank:
        fact.generateSquareIcon(16, rank.getColor(), f'rank{rank.value}.png')

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testIconFactory()
