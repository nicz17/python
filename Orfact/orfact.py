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

def main():
    log('Welcome to Orfact v' + __version__)
    testOrtifactGen()
    testPalette()

main()
