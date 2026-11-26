"""
Module to generate basic icon images.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.1.0"

import logging
from PIL import Image


class IconFactory():
    """Class IconFactory"""
    log = logging.getLogger('IconFactory')

    def __init__(self):
        """Constructor."""
        pass

    def generateSquareIcon(self, size: int, color: str) -> Image.Image:
        """Generate a monochrome square icon"""
        self.log.info(f'Generating {size}x{size} square icon color {color}')
        rgb = self.hexToRGB(color)
        self.log.debug(f'Color as RGB: {rgb}')
        img = Image.new('RGB', (size, size), rgb)
        return img

    def hexToRGB(self, hex: str):
        """Transform a hex color code to a RGB triplet."""
        shex = hex.lstrip('#')
        rgb = tuple(int(shex[i:i+2], 16) for i in (0, 2, 4))
        return rgb

    def __str__(self):
        return 'IconFactory'


def testIconFactory():
    """Unit test for IconFactory"""
    IconFactory.log.info("Testing IconFactory")
    fact = IconFactory()
    fact.generateSquareIcon(16, '#4217f0')

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testIconFactory()
