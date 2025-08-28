"""Set game playmat."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
import tkinter as tk
from tkinter import font as tkfont
from tkinter import PhotoImage

from card import Card
from player import Player
from renderer import Renderer, Meeple

class Playmat():
    """A Set game playmat."""
    log = logging.getLogger('Playmat')
    colorBg = '#006400'
    colorFg = '#127812'
    colorBd = '#004000'
    cardw = 200
    cardh = 300
    margin = 20

    def __init__(self, width: int, height: int, cbkCardSelection, cbkPlayerSelection):
        """Constructor."""
        self.width = width
        self.height = height
        self.canvas = None
        self.renderer = Renderer()
        self.cardBoxes = []
        self.playerBoxes = []
        self.cardBackId = None
        self.imgCardBack = None
        self.cbkCardSelection = cbkCardSelection
        self.cbkPlayerSelection = cbkPlayerSelection

    def addPlayers(self, players: list[Player]):
        """Display player boxes on the playmat."""
        self.log.info(f'Adding {len(players)} players to playmat')
        for i, player in enumerate(players):
            box = PlayerBox(player, self.canvas, i)
            box.render()
            self.playerBoxes.append(box)

    def addCards(self, cards: list[Card]):
        """Display cards on the playmat."""
        self.reset()
        self.log.info(f'Adding {len(cards)} cards to playmat')
        for iCard, card in enumerate(cards):
            x = self.margin + ((iCard % 4)+1)*(self.cardw + self.margin) + 100
            y = self.margin + int(iCard/4)*(self.cardh + self.margin)
            cardBox = CardBox(card, self.canvas, x, y)
            cardBox.render()
            self.cardBoxes.append(cardBox)

    def render(self):
        """Render the initial game state."""
        tx = self.cardw/2 + self.margin
        ty = self.height/2 + self.cardh/2 + 18
        self.canvas.create_text(tx, 100, fill=self.colorFg, font=self.fontBg, text='SET')
        self.imgCardBack = PhotoImage(file=f'images/cardback.png')
        self.cardBackId = self.canvas.create_image(tx, self.height/2, anchor=tk.CENTER, image=self.imgCardBack)
        self.txtDeck = self.canvas.create_text(tx, ty, fill=self.colorFg, font=self.fontFg, text='Pioche')

    def updateState(self, deckSize: int):
        """Update to the current game state."""
        self.canvas.itemconfigure(self.txtDeck, text=f'Pioche : {deckSize} cartes')
        if deckSize == 0:
            self.canvas.itemconfigure(self.txtDeck, text=f'Pioche vide')
            self.canvas.delete(self.cardBackId)
        for playerBox in self.getPlayerBoxes():
            playerBox.updateState()

    def renderCardRect(self, cx: int, cy: int):
        """Render a card placement rectangle."""
        self.canvas.create_rectangle(cx-self.cardw/2, cy-self.cardh/2, cx+self.cardw/2, cy+self.cardh/2, outline=self.colorBd)

    def reset(self):
        """Reset the playmat."""
        for box in self.getCardBoxes():
            box.dispose()
        self.cardBoxes = []

    def deleteHighlights(self):
        """Delete the highlights on the grid canvas."""
        for box in self.getCardBoxes():
            box.deleteHighlight()

    def unselectCard(self, card: Card):
        """Unselect the card. Remove its highlight."""
        for box in self.getCardBoxes():
            if box.getCard() == card:
                box.deleteHighlight()
                return
        self.log.error(f'Could not find card to unselect: {card}')
        
    def onClick(self, event: tk.Event):
        """Canvas click event callback."""
        for box in self.getCardBoxes():
            if box.contains(event.x, event.y):
                card = box.getCard()
                self.log.info(f'Clicked [{event.x}:{event.y}] on {card}')
                box.addHighlight('red')
                self.cbkCardSelection(card)
                return
        for playerBox in self.getPlayerBoxes():
            if playerBox.contains(event.x, event.y):
                self.log.info(f'Clicked [{event.x}:{event.y}] on {playerBox}')
                self.cbkPlayerSelection(playerBox.getPlayer())
                return
    
    def getCardBoxes(self) -> list['CardBox']:
        return self.cardBoxes
    
    def getPlayerBoxes(self) -> list['PlayerBox']:
        return self.playerBoxes
    
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


class CardBox():
    """A box displaying a card and its highlight."""
    log = logging.getLogger('CardBox')
    width  = Playmat.cardw
    height = Playmat.cardh

    def __init__(self, card: Card, parent: tk.Canvas, x: int, y: int):
        """Constructor with card and position."""
        self.card = card
        self.parent = parent
        self.x = x
        self.y = y
        self.img = None
        self.idImg = None
        self.idHighlight = None

    def render(self):
        """Render this card box on the parent canvas."""
        self.img = PhotoImage(file=f'images/{self.card.getImageFilename()}')
        self.idImg = self.parent.create_image(self.x, self.y, anchor=tk.NW, image=self.img)

    def dispose(self):
        """Delete all images and highlights."""
        self.parent.delete(self.idImg)
        self.parent.delete(self.idHighlight)

    def addHighlight(self, color: str):
        """Add a highlight frame."""
        self.parent.delete(self.idImg)
        self.deleteHighlight()
        self.idHighlight = self.parent.create_rectangle(self.x-4, self.y-4, 
            self.x+self.width+4, self.y+self.height+4, fill=color, outline=color)
        self.idImg = self.parent.create_image(self.x, self.y, anchor=tk.NW, image=self.img)

    def deleteHighlight(self):
        """Delete any highlights."""
        if self.idHighlight is not None:
            self.parent.delete(self.idHighlight)

    def contains(self, x: int, y: int):
        """Check if this box contains the click location."""
        return x >= self.x and x < self.x + self.width and y >= self.y and y < self.y + self.height
    
    def getCard(self) -> Card:
        """Get the card displayed in this box."""
        return self.card

    def __str__(self):
        return f'CardBox for {self.card}'


class PlayerBox():
    """A box displaying the player name, icon and score."""
    log = logging.getLogger('PlayerBox')
    width  = 200
    height = 200
    margin = 20
    colorBg = '#127812'
    colorFg = '#005600'

    def __init__(self, player: Player, parent: tk.Canvas, iy: int):
        self.player = player
        self.parent = parent
        self.iy = iy
        self.fontFg = tkfont.Font(family="Helvetica", size=24, weight='bold')
        self.icon = None
        self.x = 1300
        self.y = self.margin + self.iy*(self.height + self.margin)
        self.txtScore = None

    def render(self):
        """Render this player box on the parent canvas."""

        # Box position
        x = self.x
        y = self.y

        # Layout
        self.parent.create_rectangle(x, y, x+self.width, y+self.height, 
                fill=self.colorBg, outline=self.colorBg)
        self.parent.create_text(x+60, y+20, anchor=tk.NW, fill=self.colorFg, 
                text=self.player.getName(), font=self.fontFg)

        # Player icon
        self.icon = self.getPlayerIcon()
        self.parent.create_image(x+10, y+10, anchor=tk.NW, image=self.icon)

        # Score
        score = f'{self.player.getScore()} points'
        self.txtScore = self.parent.create_text(x+10, y+80, anchor=tk.NW, 
                fill=self.colorFg, text=score, font=self.fontFg)

    def updateState(self):
        """Update player score."""
        score = f'{self.player.getScore()} points'
        self.parent.itemconfigure(self.txtScore, text=score)

    def getPlayer(self) -> Player:
        """Returns the player in this box."""
        return self.player
    
    def getPlayerIcon(self) -> PhotoImage:
        """Get or generate the player meeple icon."""
        filename = self.player.getImage()
        if not os.path.exists(filename):
            self.log.info(f'Generating player icon {filename}')
            meeple = Meeple(self.player.getColor())
            meeple.render(filename)
        return PhotoImage(file=filename)

    def contains(self, x: int, y: int):
        """Check if this box contains the click location."""
        return x >= self.x and x < self.x + self.width and y >= self.y and y < self.y + self.height

    def __str__(self):
        return f'PlayerBox for {self.player}'