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
    colorFg = '#127812'
    colorBd = '#004000'
    cardw = 200
    cardh = 300
    margin = 20

    def __init__(self, width: int, height: int, cbkCardSelection):
        """Constructor."""
        self.width = width
        self.height = height
        self.canvas = None
        self.renderer = Renderer()
        self.cardImages = {}
        self.cardPositions = {}
        self.aHighlightIds = []
        self.cardImageIds = []
        self.cardBackId = None
        self.cbkCardSelection = cbkCardSelection

    def addCards(self, cards: list[Card]):
        """Display cards on the playmat."""
        self.reset()
        self.log.info(f'Adding {len(cards)} cards to playmat')
        for iCard, card in enumerate(cards):
            filename = self.renderer.getImageFilename(card)
            #self.log.info(f'Display card image {filename}')
            img = PhotoImage(file=f'images/{filename}')
            self.cardImages[card] = img
            x = self.margin + ((iCard % 4)+1)*(self.cardw + self.margin) + 100
            y = self.margin + int(iCard/4)*(self.cardh + self.margin)
            id = self.canvas.create_image(x, y, anchor=tk.NW, image=img)
            self.cardPositions[card] = (x, y)
            self.cardImageIds.append(id)

    def render(self):
        """Render the initial game state."""
        self.canvas.create_text(110, 100, fill=self.colorFg, font=self.fontBg, text='SET')
        ty = self.height/2 + self.cardh/2 + 18
        self.txtDeck = self.canvas.create_text(110, ty, fill=self.colorFg, font=self.fontFg, text='Pioche')
        #self.renderCardRect(110, self.height/2)
        imgCardBack = PhotoImage(file=f'images/cardback.png')
        self.cardImages['back'] = imgCardBack
        self.cardBackId = self.canvas.create_image(110, self.height/2, anchor=tk.CENTER, image=imgCardBack)

    def updateState(self, deckSize: int):
        """Update to the current game state."""
        self.canvas.itemconfigure(self.txtDeck, text=f'Pioche : {deckSize} cartes')
        if deckSize == 0:
            self.canvas.itemconfigure(self.txtDeck, text=f'Pioche vide')
            self.canvas.delete(self.cardBackId)


    def renderCardRect(self, cx: int, cy: int):
        """Render a card placement rectangle."""
        self.canvas.create_rectangle(cx-self.cardw/2, cy-self.cardh/2, cx+self.cardw/2, cy+self.cardh/2, outline=self.colorBd)

    def drawHighlight(self, card: Card, color: str):
        """Draw a highlight rectangle for the specified card."""

        # Draw highlight rectangle
        (x, y) = self.cardPositions[card]
        id = self.canvas.create_rectangle(x-4, y-4, x+self.cardw+4, y+self.cardh+4, fill=color, outline=color)
        self.aHighlightIds.append(id)
        
        # Redraw card image
        img = self.cardImages[card]
        id = self.canvas.create_image(x, y, anchor=tk.NW, image=img)
        self.cardImageIds.append(id)

    def reset(self):
        """Reset the playmat."""
        self.cardPositions = {}
        for id in self.cardImageIds:
            self.canvas.delete(id)
        self.cardImageIds = []
        self.deleteHighlights()

    def deleteHighlights(self):
        """Delete the highlights on the grid canvas."""
        for id in self.aHighlightIds:
            self.canvas.delete(id)
        self.aHighlightIds = []
        
    def onClick(self, event):
        """Canvas click event callback."""
        card = self.getCardAt(event.x, event.y)
        self.log.info(f'Click at {event.x}:{event.y} is {card}')
        if card:
            self.drawHighlight(card, 'red')
            self.cbkCardSelection(card)

    def getCardAt(self, x: int, y: int) -> Card:
        """Gets the card at position x, y or None if no card there."""
        for card, pos in self.cardPositions.items():
            cx = pos[0]
            cy = pos[1]
            if x >= cx and x < cx + self.cardw and y >= cy and y < cy + self.cardh:
                return card
        return None
    
    def createWidgets(self, parent: tk.Frame):
        # Canvas
        self.canvas = tk.Canvas(master=parent, bg=self.colorBg, bd=2, 
                                height=self.height, width=self.width, 
                                highlightthickness=2, highlightbackground=self.colorBd)
        self.canvas.bind("<Button-1>", self.onClick)
        self.canvas.pack(side=tk.LEFT)

        # Fonts
        self.fontBg = tkfont.Font(family="Helvetica", size=42)
        self.fontFg = tkfont.Font(family="Helvetica", size=16, weight='bold')
        