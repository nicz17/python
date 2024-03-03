"""
A simple UML parser.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from SimpleUMLClass import *


class SimpleUMLParser():
    """A simple UML parser."""
    log = logging.getLogger('SimpleUMLParser')

    def __init__(self, lang: str) -> None:
        """Constructor with language."""
        self.log.info('Constructor, language: %s', lang)
        self.lang = lang

    def parse(self, filename: str):
        """Parse the specified text file."""
        self.log.info('Parsing %s', filename)

