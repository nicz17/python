"""
 A random artifact factory
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import sys

from NameGen import *
from Ortifact import *
from OrtifactGen import *
from Palette import *
from ImageMask import *
from DemoImageMask import *
from DemoPalette import *
from HtmlPage import *

def log(msg):
    print(msg, file=sys.stdout, flush=True)

def testNameGen():
    nGen = 8
    log('Generating ' + str(nGen) + ' names')
    nameGen = NameGen(42)
    for i in range(nGen):
        log(nameGen.generate())

def testOrtifactGen():
    nGen = 8
    log('Generating ' + str(nGen) + ' ortifacts')
    ogen = OrtifactGen(42)
    for i in range(nGen):
        ortifact = ogen.generate()
        log(ortifact)

def testPalette():
    log('Testing palette')
    pal = HeatPalette()
    pal.toColorScale('HeatPalette.png', 800, 50)
    pal = LinesPalette()
    pal.toColorScale('LinesPalette.png', 800, 50)
    pal = RandomPalette()
    pal.toColorScale('RandomPalette.png', 800, 50)

def testHtmlPage():
    log('Testing HtmlPage')
    page = HtmlPage('ImageMasks', 'orfact.css')
    page.addHeading(1, 'Image generation tests')

    page.addHeading(2, 'Palettes')
    aNames = ['HeatPalette', 'LinesPalette', 'RandomPalette']
    aPalImgs = []
    for sName in aNames:
        aPalImgs.append(ImageHtmlTag(sName + '.png', sName))
    page.addTable(aPalImgs, 1)

    page.addHeading(2, 'Image Masks')
    aMaskImgs = []
    aMaskImgs.append(ImageHtmlTag('ImageMask-grayscale.png', 'Grayscale'))
    aMaskImgs.append(ImageHtmlTag('ImageMask-heat.png', 'Heat palette'))
    aMaskImgs.append(ImageHtmlTag('ImageMask-lines.png', 'Lines palette'))
    aMaskImgs.append(ImageHtmlTag('ImageMask-random.png', 'Random palette'))
    page.addTable(aMaskImgs, 4)

    page.addHeading(2, 'Random names')
    nameGen = NameGen(42)
    aNames = []
    for i in range(12):
        aNames.append(HtmlTag('p', nameGen.generate()))
    page.addTable(aNames)

    page.save('Images.html')

def testImageMaskInternal():
    log('Testing ImageMask internals')
    mask = GaussImageMask(5, 3)
    mask.generate()
    print(mask.aMask)

def testImageMask():
    log('Testing ImageMask')
    size = 250
    oPalette = RandomPalette()
    oPalette.toColorScale('RandomPalette.png', 800, 50)
    mask = ManhattanImageMask(300, 200)
    mask.generate()
    mask.toGrayScale('ImageMask-grayscale.png')
    mask.toImage(oPalette, 'ImageMask-random.png')
    mask.toImage(HeatPalette(), 'ImageMask-heat.png')
    mask.toImage(LinesPalette(), 'ImageMask-lines.png')

def runTests():
    testOrtifactGen()
    testPalette()
    testImageMaskInternal()
    testImageMask()
    testHtmlPage()

def runDemos():
    DemoPalette().run()
    DemoImageMask().run()

def main():
    log('Welcome to Orfact v' + __version__)
    #runTests()
    runDemos()

main()
