"""
 The Mandelbrot set fractal.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging

class MandelbrotSet:
    """The Mandelbrot set fractal."""
    log = logging.getLogger('MandelbrotSet')

    def __init__(self, iMaxIter, rBailout):
        self.log.info('Mandelbrot set with %d iterations and %.1f bailout', iMaxIter, rBailout)
        self.iMaxIter = iMaxIter
        self.rBailout = rBailout

    def iter(self, z):
        """Compute the iterations required to bailout at complex number z."""
        c = z
        for i in range(self.iMaxIter):
            z = z*z + c
            if abs(z) > self.rBailout:
                return i
        return self.iMaxIter
    
    def getDefaultCenter(self):
        return complex(-0.75, 0.0)
    
    def __str__(self):
        return 'Mandelbrot set with ' + str(self.iMaxIter) + ' iterations'
    
    

class JuliaSet:
    """The Julia set fractal."""
    log = logging.getLogger('JuliaSet')

    def __init__(self, iMaxIter, rBailout):
        self.log.info('Julia set with %d iterations and %.1f bailout', iMaxIter, rBailout)
        self.iMaxIter = iMaxIter
        self.rBailout = rBailout
        self.c = complex(-0.73756, -0.16869)

    def iter(self, z):
        """Compute the iterations required to bailout at complex number z."""
        for i in range(self.iMaxIter):
            z = z*z + self.c
            if abs(z) > self.rBailout:
                return i
        return self.iMaxIter
    
    def getDefaultCenter(self):
        return complex(0.0, 0.0)
    
    def __str__(self):
        return 'Julia set with ' + str(self.iMaxIter) + ' iterations'


class BurningShip:
    """The Burning Ship fractal."""
    log = logging.getLogger('BurningShip')

    def __init__(self, iMaxIter, rBailout):
        self.log.info('Burning Ship with %d iterations and %.1f bailout', iMaxIter, rBailout)
        self.iMaxIter = iMaxIter
        self.rBailout = rBailout

    def iter(self, z):
        """Compute the iterations required to bailout at complex number z."""
        c = z
        for i in range(self.iMaxIter):
            az = complex(abs(z.real), abs(z.imag))
            z = az*az + c
            if abs(z) > self.rBailout:
                return i
        return self.iMaxIter
    
    def getDefaultCenter(self):
        return complex(0.0, 0.0)
    
    def __str__(self):
        return 'Burning Ship with ' + str(self.iMaxIter) + ' iterations'
