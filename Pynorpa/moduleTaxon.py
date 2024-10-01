"""
 Pynorpa Module for displaying and editing taxa.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from TabsApp import *
from BaseTree import *


class ModuleTaxon(TabModule):
    """Pynorpa Module for taxa."""
    log = logging.getLogger('ModuleTaxon')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        super().__init__(parent, 'Taxons')
        self.tree = BaseTree(self.onSelectTaxon)

    def loadData(self):
        self.tree.addTestItems()

    def onSelectTaxon(self, taxon):
        #self.log.info(f'Selected {taxon}')
        self.log.info(f'Selected {self.tree.getSelectedId()}')
        # Display in widgets
        #self.editor.loadData(taxon)

    def createWidgets(self):
        """Create user widgets."""

        # Frames
        self.frmLeft = tk.Frame(master=self.oFrame)
        self.frmLeft.pack(fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight = tk.Frame(master=self.oFrame)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=6, padx=6)

        # Location widgets
        self.tree.createWidgets(self.frmLeft)
        #self.editor.createWidgets(self.frmRight)