"""
A factory to generate synthetic values.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import io
import logging
import math
import random
import numpy  as np
import pandas as pd

    
class ValuesGenerator:
    """Generate an array of values."""
    log = logging.getLogger('ValuesGenerator')

    def __init__(self):
        pass

    def generate(self, nValues: int):
        """Generate an array of values and return it."""
        self.log.info(f'Generating array of {nValues} values')
        return np.repeat(0.0, nValues)

    def setIndex(self, index):
        """Set the Pandas dataframe index for some subclasses."""
        pass

    def interpolate(self, low: float, high: float, frac: float):
        """Interpolate at the specified fraction (0 to 1) between low and high."""
        return low + frac*(high - low)

    def __str__(self):
        return f'ValuesGenerator'
    
class ValuesGeneratorConst(ValuesGenerator):
    """Generate an array of constant values."""
    log = logging.getLogger('ValuesGeneratorConst')

    def __init__(self, value: float):
        super().__init__()
        self.value = value

    def generate(self, nValues: int):
        self.log.info(f'Generating {nValues} constant values {self.value}')
        return np.repeat(self.value, nValues)

    def __str__(self):
        return f'ValuesGeneratorConst'
    
class ValuesGeneratorNoise(ValuesGenerator):
    """Generate random noise values."""
    log = logging.getLogger('ValuesGeneratorNoise')

    def __init__(self, ampl: float):
        super().__init__()
        self.ampl = ampl

    def generate(self, nValues: int):
        self.log.info(f'Generating {nValues} random noise values {self.ampl}')
        return np.random.uniform(low=-self.ampl, high=self.ampl, size=(nValues,))

    def __str__(self):
        return f'ValuesGeneratorNoise'

class ValuesGeneratorOscillator(ValuesGenerator):
    """Generate sine wave values between low and high at the specified frequency."""
    log = logging.getLogger('ValuesGeneratorOscillator')

    def __init__(self, low: float, high: float, freq: float, phi0=0.0):
        super().__init__()
        self.low = low
        self.high = high
        self.freq = freq
        self.phi0 = phi0

    def generate(self, nValues: int):
        ampl = (self.high - self.low)/2
        mean = (self.high + self.low)/2
        self.log.info(f'Generating {nValues} oscillating values at {mean} +- {ampl}')
        values = []
        for x in range(nValues):
            values.append(mean + ampl*math.sin(x*self.freq + self.phi0))
        return values

    def __str__(self):
        return f'ValuesGeneratorOscillator'

class ValuesGeneratorOperation(ValuesGenerator):
    """Sets the value to 1 between 08:00 and 17:00, else 0."""
    log = logging.getLogger('ValuesGeneratorOperation')

    def __init__(self, low=8.0, high=17.0, value=1.0):
        super().__init__()
        self.low  = low
        self.high = high
        self.value = value
        self.index = None

    def setIndex(self, index):
        """Set the Pandas dataframe index for some subclasses."""
        self.index = index
        if index is not None:
            self.log.debug(f'Type of index: {index.inferred_type}')

    def generate(self, nValues: int):
        self.log.info(f'Generating {nValues} operation values from {self.low} to {self.high}')
        values = []
        for i in range(nValues):
            hour = 0
            if self.index.inferred_type == 'integer':
                hour = self.index[i]
            elif self.index.inferred_type == 'datetime64':
                hour = self.index[i].hour
            values.append(self.value if hour >= self.low and hour < self.high else 0.0)
        return values

    def __str__(self):
        return f'ValuesGeneratorOperation'
    
class IndexGenerator:
    """Generate an integer dataframe index."""
    log = logging.getLogger('IndexGenerator')

    def __init__(self):
        pass

    def generate(self, nValues: int):
        self.log.info(f'Generating index with {nValues} integer values')
        return np.arange(1, nValues+1)

    def __str__(self):
        return f'IndexGenerator'

class IndexGeneratorDate(IndexGenerator):
    """Generate a datetime dataframe index."""
    log = logging.getLogger('IndexGeneratorDate')

    def __init__(self, freq='1D', start='2026-01-01'):
        self.freq = freq
        self.start = start
        super().__init__()

    def generate(self, nValues: int):
        self.log.info(f'Generating index with {nValues} values from {self.start} freq {self.freq}')
        return pd.date_range(start=self.start, periods=nValues, freq=self.freq)

    def __str__(self):
        return f'IndexGeneratorDate from {self.start} freq {self.freq}'


class ValuesFactory:
    """Factory for generating synthetic values."""
    log = logging.getLogger('ValuesFactory')

    def __init__(self, name: str, nValues: int) -> None:
        """Constructor with model name, number of values to generate."""
        self.name = name
        self.nValues = nValues
        self.df = pd.DataFrame()
        self.indexgen = IndexGenerator()
        self.valuegens = []
        self.log.debug(f'Constructor {self}')

    def generate(self):
        """Create a Pandas Dataframe and fill it with synthetic values."""
        self.log.info(f'Generating {self.name} DataFrame with {self.nValues} values')
        self.df = pd.DataFrame({
                "value": np.repeat(0.0, self.nValues)
            },
            index = self.buildIndex()
            )
        self.df.index.name = 'index'
        self.generateValues()
        self.log.debug('Dataframe:\n%s', self.df)

    def addValuesGen(self, gen: ValuesGenerator):
        """Add a values generator."""
        self.valuegens.append(gen)

    def setValuesGenerators(self, gens: list):
        """Set the values generators."""
        self.valuegens = gens

    def setIndexGen(self, gen: IndexGenerator):
        """Set the index generator."""
        self.indexgen = gen

    def buildIndex(self):
        """Generate the dataframe index."""
        return self.indexgen.generate(self.nValues)

    def generateValues(self):
        """Generate the required number of values."""
        self.log.info(f'Adding {self.nValues} values using {len(self.valuegens)} generators')
        values = np.repeat(0.0, self.nValues)
        for gen in self.valuegens:
            gen.setIndex(self.df.index)
            values = np.add(values, gen.generate(self.nValues))
        self.df.value = values

    def saveAsCSV(self):
        """Save the DataFrame to a CSV file."""
        filename = f'{self.name}.csv'
        self.log.info(f'Saving synthetic data to {filename}')
        self.df.to_csv(filename)

    def saveAsOpitCSV(self):
        """Saves the generated data as an OPIT export CSV file."""
        filename = f'{self.name}.csv'
        self.log.info(f'Saving in OPIT format to {filename}')
        with open(filename, 'w') as file:
            file.write(self.createHeader())
            self.df.to_csv(file, sep=',', header=False)

    def createHeader(self) -> str:
        """Create a CSV file header."""
        header = io.StringIO()
        header.write(f'SourceName,SrcValuesGenerator\n')
        header.write(f'DPName,DpValuesGenerator\n')
        header.write(f'Source,ValuesFactory.py\n')
        header.write(f'Location,localhost\n')
        header.write(f'Description,{self}\n')
        header.write(f'Unit,kWh\n')
        header.write(f'PrimaryKey,{self.getRandomPrimaryKey()}\n')
        header.write(f'Timestamp:\n')
        return header.getvalue()
    
    def getRandomPrimaryKey(self):
        return random.randint(10000, 99999)

    def __str__(self):
        return f'ValuesFactory {self.name}'


def testValuesFactory():
    """Unit test for ValuesFactory."""
    fact = ValuesFactory('SimpleTest', 24)
    fact.setIndexGen(IndexGeneratorDate('1h', '2026-05-27'))
    fact.setValuesGenerators([
        ValuesGeneratorConst(42.0),
        ValuesGeneratorOscillator(-5.0, 5.0, 2.0*math.pi/24.0, math.pi),
        ValuesGeneratorNoise(0.5),
        #ValuesGeneratorOperation(8.0, 18.0, 100)
    ])
    fact.generate()
    #fact.saveAsCSV()
    fact.saveAsOpitCSV()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testValuesFactory()