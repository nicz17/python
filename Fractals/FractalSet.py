"""
 Various factal sets:
 Mandelbrot, Julia, Burning Ship etc.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import cmath

class FractalSet:
    """A fractal set interface."""
    log = logging.getLogger('FractalSet')

    def __init__(self, sName, iMaxIter, rBailout = 2.0):
        self.log.info('%s with %d iterations and %.1f bailout', sName, iMaxIter, rBailout)
        self.sName = sName
        self.iMaxIter = iMaxIter
        self.rBailout = rBailout

    def iter(self, z):
        """Compute the iterations required to bailout at complex number z."""
        return self.iMaxIter
    
    def getDefaultCenter(self) -> complex:
        return complex(0.0, 0.0)
    
    def getDefaultWidth(self) -> float:
        return 3.0
    
    def __str__(self):
        return self.sName + ' with ' + str(self.iMaxIter) + ' iterations'
    

class MandelbrotSet(FractalSet):
    """The Mandelbrot set fractal."""
    log = logging.getLogger('MandelbrotSet')

    def __init__(self, iMaxIter, rBailout = 2.0):
        super().__init__('Mandelbrot set', iMaxIter, rBailout)

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
    

class JuliaSet(FractalSet):
    """The Julia set fractal."""
    log = logging.getLogger('JuliaSet')

    def __init__(self, iMaxIter, rBailout = 2.0):
        super().__init__('Julia set', iMaxIter, rBailout)
        self.c = complex(-0.73756, -0.16869)

    def iter(self, z):
        """Compute the iterations required to bailout at complex number z."""
        for i in range(self.iMaxIter):
            z = z*z + self.c
            if abs(z) > self.rBailout:
                return i
        return self.iMaxIter
    

class BurningShip(FractalSet):
    """The Burning Ship fractal."""
    log = logging.getLogger('BurningShip')

    def __init__(self, iMaxIter, rBailout = 2.0):
        super().__init__('Burning Ship', iMaxIter, rBailout)

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
        return complex(0.0, -0.5)
    
    def getDefaultWidth(self) -> float:
        return 4.0


class LogisticMap(FractalSet):
    """The logistic map fractal, or fish fractal."""
    log = logging.getLogger('LogisticMap')

    def __init__(self, iMaxIter, rBailout = 2.0):
        super().__init__('Logistic map', iMaxIter, rBailout)

    def iter(self, z):
        """Compute the iterations required to bailout at complex number z."""
        c = z
        for i in range(self.iMaxIter):
            z = c*z*(1.0 - z)
            if abs(z) > self.rBailout:
                return i
        return self.iMaxIter


class SineFractal(FractalSet):
    """Sine fractal."""
    log = logging.getLogger('SineFractal')

    def __init__(self, iMaxIter, rBailout = 31.415):
        super().__init__('Sine fractal', iMaxIter, rBailout)

    def iter(self, z):
        """Compute the iterations required to bailout at complex number z."""
        c = z
        for i in range(self.iMaxIter):
            z = cmath.sin(z) + c
            if abs(z) > self.rBailout:
                return i
        return self.iMaxIter
    
    def getDefaultWidth(self) -> float:
        return 6.3


class DucksFractal(FractalSet):
    """The Ducks fractal. See http://www.algorithmic-worlds.net/blog/blog.php?Post=20110227"""
    log = logging.getLogger('DucksFractal')

    def __init__(self, iMaxIter, rBailout = 2.0):
        super().__init__('Ducks fractal', iMaxIter, rBailout)

    def iter(self, z):
        #c = z
        c = complex(0.0001, 0.0001)
        try:
            for i in range(self.iMaxIter):
                az = complex(z.real, abs(z.imag))
                z = cmath.log(az + c)
                if abs(z) > self.rBailout:
                    return i
        except:
            pass
        return self.iMaxIter
    
    def getDefaultCenter(self):
        return complex(0.0, 0.0)
    
    def getDefaultWidth(self) -> float:
        return 4.0