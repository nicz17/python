"""
A model to generate synthetic values.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import numpy  as np
import pandas as pd

class Model:
    """Interface for generating synthetic values."""
    log = logging.getLogger(__name__)

    def __init__(self, name: str, nValues: int, dOptions: dict) -> None:
        self.name = name
        self.nValues = nValues
        self.dOptions = dOptions
        self.df = None
        self.log.info('Model %s', name)

    def createDataframe(self):
        """
        Create a Pandas Dataframe and fill it with synthetic values.
        """
        self.log.info('Generating DataFrame with %d %s values', self.nValues, self.name)
        self.df = pd.DataFrame({
                "day": np.arange(1, self.nValues+1),
                "value": self.generate()
            },
            index = self.buildIndex()
            )
        self.df.index.name = 'index'
        if self.dOptions['verbose']:
            self.log.info('Dataframe:\n%s', self.df)

    def buildIndex(self):
        """Generate the dataframe index."""
        return pd.date_range(start='01/01/2023', periods = self.nValues)

    def generate(self):
        """Generate the specified number of values."""
        pass

    def noise(self, ampl: float):
        """Generate a random noise array"""
        return np.random.uniform(low=-ampl, high=ampl, size=(self.nValues,))

    def saveAsCSV(self):
        """Save the DataFrame to a CSV file."""
        sFilename = f'{self.name}.csv'
        self.log.info('Saving synthetic data to %s', sFilename)
        self.df.to_csv(sFilename)

class RandomModel(Model):
    """A model generating random values."""

    def __init__(self, nValues: int, dOptions: dict) -> None:
        super().__init__('RandomModel', nValues, dOptions)

    def generate(self):
        self.log.info('Generating %d %s values', self.nValues, self.name)
        return np.random.rand(self.nValues)
    
class ConstantModel(Model):
    """A model generating constant values with random noise."""

    def __init__(self, nValues: int, value: float, dOptions: dict) -> None:
        super().__init__('ConstantModel', nValues, dOptions)
        self.value = value

    def generate(self):
        self.log.info('Generating %d %s values', self.nValues, self.name)
        arrConst = np.repeat(self.value, self.nValues)
        arrNoise = self.noise(0.9)
        return np.add(arrConst, arrNoise)
    
class ConsumptionModel(Model):
    """A model generating high/low consumption values with random noise."""

    def __init__(self, nValues: int, valLow: float, valHigh: float, dOptions: dict) -> None:
        super().__init__('ConsumptionModel', nValues, dOptions)
        self.valLow  = valLow
        self.valHigh = valHigh

    def generate(self):
        self.log.info('Generating %d %s values', self.nValues, self.name)
        arrConst = []
        for i in range(self.nValues):
            if i > 10 and i < 20:
                arrConst.append(self.valHigh)
            else:
                arrConst.append(self.valLow)
        arrNoise = self.noise(0.9)
        return np.add(arrConst, arrNoise)