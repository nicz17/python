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
    pal = OraVioPalette()
    pal.toColorScale('OraVioPalette.png', 800, 50)
    pal = RandomPalette()
    pal.toColorScale('RandomPalette.png', 800, 50)

def testHtmlPage():
    log('Testing HtmlPage')
    page = HtmlPage('Test', 'orfact.css')
    page.addHeading(1, 'Image generation tests')

    page.addHeading(2, 'Palettes')
    aNames = ['HeatPalette', 'OraVioPalette', 'RandomPalette']
    aPalImgs = []
    for sName in aNames:
        tImg = HtmlTag('img')
        tImg.addAttr('src', sName + '.png')
        tImg.addAttr('title', sName)
        aPalImgs.append(tImg)
    page.addTable(aPalImgs, 1)

    page.addHeading(2, 'Random names')
    nameGen = NameGen(42)
    aNames = []
    for i in range(12):
        aNames.append(HtmlTag('p', nameGen.generate()))
    page.addTable(aNames)

    page.save('Images.html')

def main():
    log('Welcome to Orfact v' + __version__)
    #testOrtifactGen()
    testPalette()
    testHtmlPage()

main()
