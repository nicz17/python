"""
Rendering for the Set game.
See https://note.nkmk.me/en/python-pillow-imagedraw/
"""

import logging
import os

from card import Card, CardColor, CardFill, CardShape
from game import Game
from PIL import Image, ImageDraw

class Renderer():
    """Renderer for the Set game."""
    log = logging.getLogger('Renderer')
    dirImages = 'images/'
    cardWidth  = 200
    cardHeight = 300
    margin = 20

    def __init__(self):
        """Constructor."""
        self.log.info(f'Constructor for {self}')

    def generateCardImages(self):
        """Generate all card images."""
        self.log.info('Generating card images')

        # Create image dir if needed
        if not os.path.isdir(self.dirImages):
            os.makedirs(self.dirImages)

        # Get the cards
        game = Game()
        game.createDeck()
        cards = game.cards

        # Generate card images
        for card in cards:
            self.generateCardImage(card)

    def generateCardImage(self, card: Card):
        """Generate a single card image."""
        filename = self.getImageFilename(card)
        self.log.info(f'Generating image for {card} as {filename}')

        # Get the shape coords
        coordsArray = self.getShapeCoords(card)

        # Get the shape colors
        outline, fill = self.getShapeColors(card)

        # Create the image
        img = Image.new('RGB', (self.cardWidth, self.cardHeight), (256, 256, 256))
        draw = ImageDraw.Draw(img)

        # Draw the shapes
        for coords in coordsArray:
            if card.shape == CardShape.Oval:
                draw.ellipse(coords, fill=fill, outline=outline, width=5)
            if card.shape == CardShape.Wave:
                draw.polygon(coords, fill=outline, outline=outline)
                coordsInner = self.getDiamondCoordsInner(coords)
                draw.polygon(coordsInner, fill=fill, outline=fill)
            else:
                draw.rectangle(coords, fill=fill, outline=outline, width=5)

        # Save the image
        img.save(f'{self.dirImages}{filename}')

    def getShapeCoords(self, card: Card):
        """Get the coordinates for drawing the shapes."""
        if card.shape == CardShape.Wave:
            return self.getDiamondCoords(card)
        
        coords = []
        x1 = self.margin
        x2 = self.cardWidth - self.margin
        sh = (self.cardHeight - 4*self.margin)/3

        if card.number == 1:
            y1 = self.cardHeight/2 - sh/2
            y2 = self.cardHeight/2 + sh/2
            coords.append((x1, y1, x2, y2))
        elif card.number == 2:
            y1 = self.cardHeight/2 - self.margin/2 - sh
            coords.append((x1, y1, x2, y1+sh))
            y1 += self.margin + sh
            coords.append((x1, y1, x2, y1+sh))
        elif card.number == 3:
            y1 = self.margin
            coords.append((x1, y1, x2, y1+sh))
            y1 += self.margin + sh
            coords.append((x1, y1, x2, y1+sh))
            y1 += self.margin + sh
            coords.append((x1, y1, x2, y1+sh))
        return coords
    
    def getDiamondCoords(self, card: Card):
        """Get the coordinates for drawing diamond shapes."""
        coords = []
        sh = (self.cardHeight - 4*self.margin)/3
        if card.number == 1:
            coords.append(self.getDiamondCoordsAt(self.cardHeight/2))
        elif card.number == 2:
            coords.append(self.getDiamondCoordsAt(self.cardHeight/2 - self.margin/2 - sh/2))
            coords.append(self.getDiamondCoordsAt(self.cardHeight/2 + self.margin/2 + sh/2))
        elif card.number == 3:
            coords.append(self.getDiamondCoordsAt(self.margin + sh/2))
            coords.append(self.getDiamondCoordsAt(self.cardHeight/2))
            coords.append(self.getDiamondCoordsAt(self.cardHeight - self.margin - sh/2))
        return coords
    
    def getDiamondCoordsAt(self, y: int):
        xl = self.margin
        xr = self.cardWidth - self.margin
        xm = self.cardWidth/2
        sh = (self.cardHeight - 4*self.margin)/3
        return ((xl, y), (xm, y - sh/2), (xr, y), (xm, y + sh/2))
    
    def getDiamondCoordsInner(self, coords):
        tx = 9
        ty = 5
        xl = coords[0][0] + tx
        xm = coords[1][0]
        xr = coords[2][0] - tx
        ym = coords[0][1]
        yt = coords[1][1] + ty
        yb = coords[3][1] - ty
        return ((xl, ym), (xm, yt), (xr, ym), (xm, yb))


    def getShapeColors(self, card: Card):
        """Get the outline and fill colors for the card."""

        # Shape colors
        if (card.color == CardColor.Red):
            outline = (255, 0, 0)
            fill    = (255, 128, 128)
        elif (card.color == CardColor.Blue):
            outline = (0, 0, 255)
            fill    = (128, 128, 255)
        else:
            outline = (0, 255, 0)
            fill    = (128, 255, 128)

        # Adapt fill color
        if (card.fill == CardFill.Empty):
            fill = (255, 255, 255)
        elif (card.fill == CardFill.Full):
            fill = outline
        
        return outline, fill

    def getImageFilename(self, card: Card) -> str:
        """Get the file name for the card image."""
        return f'{card.shape.name}{card.color.name}{card.fill.name}{card.number}.png'

    def __str__(self):
        return 'Renderer'
    

def testRenderer():
    renderer = Renderer()
    renderer.generateCardImages()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testRenderer()