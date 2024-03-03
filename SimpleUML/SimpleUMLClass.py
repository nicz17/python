"""
A simple code generator.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
import DateTools


class SimpleUMLClass():
    """A simple class."""
    log = logging.getLogger('SimpleUMLClass')

    def __init__(self) -> None:
        """Constructor."""
        self.log.info('Constructor')
