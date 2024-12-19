"""Cassino game playmat."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import font as tkfont
import logging

class Playmat():
    """A Cassino playmat."""
    log = logging.getLogger('Playmat')
    colorBg = '#006400'
    colorFg = '#107410'
    colorBd = '#004000'
    cardw = 100
    cardh = 160

    def __init__(self, width: int, height: int):
        """Constructor."""
        self.width = width
        self.height = height
        self.canvas = None

    def render(self):
        """Render the current game state."""
        msgId = self.canvas.create_text(self.width/2, self.height/2, fill=self.colorFg, font=self.fontBg, text='CASSINO')
        self.canvas.create_text(100, self.height/2, fill=self.colorBd, text='Pioche')
        self.renderCardRect(100, self.height/2)

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
        