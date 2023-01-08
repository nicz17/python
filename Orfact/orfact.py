import sys
from NameGen import *
from Ortifact import *
from OrtifactGen import *

sVersion = '1.0.0'

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

def main():
    log('Welcome to Orfact v' + sVersion)
    testOrtifactGen()

main()
