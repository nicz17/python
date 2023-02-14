"""
 The Mandelbrot set fractal.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging

class MandelbrotSet:
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
    
    def __str__(self):
        return 'Mandelbrot set with ' + str(self.iMaxIter) + ' iterations'