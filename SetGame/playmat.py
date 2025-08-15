"""Set game playmat."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import font as tkfont
from tkinter import PhotoImage

from card import Card
from renderer import Renderer

class Playmat():
    """A Set game playmat."""
    log = logging.getLogger('Playmat')
    colorBg = '#006400'
    colorFg = '#107410'
    colorBd = '#004000'
    cardw = 200
    cardh = 300
    margin = 20

    def __init__(self, width: int, height: int):
        """Constructor."""
        self.width = width
        self.height = height
        self.canvas = None
        self.renderer = Renderer()
        self.cardImages = {}

    def addCards(self, cards: list[Card]):
        """Display cards on the playmat."""
        self.log.info(f'Adding {len(cards)} cards to playmat')
        for iCard, card in enumerate(cards):
            filename = self.renderer.getImageFilename(card)
            self.log.info(f'Display card image {filename}')
            img = PhotoImage(file=f'images/{filename}')
            self.cardImages[card] = img
            x = self.margin + ((iCard % 4)+1)*(self.cardw + self.margin) + 100
            y = self.margin + int(iCard/4)*(self.cardh + self.margin)
            id = self.canvas.create_image(x, y, anchor=tk.NW, image=img)

    def render(self):
        """Render the current game state."""
        msgId = self.canvas.create_text(110, 100, fill=self.colorFg, font=self.fontBg, text='SET')
        self.canvas.create_text(110, self.height/2, fill=self.colorBd, text='Pioche')
        self.renderCardRect(110, self.height/2)
        imgCardBack = PhotoImage(file=f'images/cardback.png')
        self.cardImages['back'] = imgCardBack
        self.canvas.create_image(110, self.height/2, anchor=tk.CENTER, image=imgCardBack)

    def renderCardRect(self, cx: int, cy: int):
        """Render a card placement rectangle."""
        self.canvas.create_rectangle(cx-self.cardw/2, cy-self.cardh/2, cx+self.cardw/2, cy+self.cardh/2, outline=self.colorBd)
    
    def createWidgets(self, parent: tk.Frame):
        # Canvas
        self.canvas = tk.Canvas(master=parent, bg=self.colorBg, bd=2, 
                                height=self.height, width=self.width, 
                                highlightthickness=2, highlightbackground=self.colorBd)
        self.canvas.pack(side=tk.LEFT)

        # Fonts
        self.fontBg = tkfont.Font(family="Helvetica", size=42)
        