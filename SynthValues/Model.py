"""
A model to generate synthetic values.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import numpy  as np
import pandas as pd
import matplotlib

class Model:
    """Interface for generating synthetic values."""
    log = logging.getLogger(__name__)

    def __init__(self, name: str, nValues: int, dOptions: dict) -> None:
        """Constructor with model name, number of values to generate, and other options."""
        self.name = name
        self.nValues = nValues
        self.dOptions = dOptions
        self.df = pd.DataFrame()
        self.log.info('Model %s', name)

    def createDataframe(self):
        """Create a Pandas Dataframe and fill it with synthetic values."""
        self.log.info('Generating DataFrame with %d %s values', self.nValues, self.name)
        self.df = pd.DataFrame({
                #"seq":   np.arange(1, self.nValues+1),
                "value": np.repeat(0, self.nValues)
            },
            index = self.buildIndex()
            )
        self.df.index.name = 'index'
        self.df.value = self.generate()
        #if self.dOptions['verbose']:
        self.log.info('Dataframe:\n%s', self.df)

    def buildIndex(self):
        """Generate the dataframe index."""
        return pd.date_range(start='01/01/2023', periods = self.nValues)

    def generate(self):
        """Generate the specified number of values."""
        pass

    def noise(self, ampl: float):
        """Generate a random noise array."""
        return np.random.uniform(low=-ampl, high=ampl, size=(self.nValues,))

    def interpolate(self, low: float, high: float, frac: float):
        """Interpolate at the specified fraction (0 to 1) between low and high."""
        return low + frac*(high - low)
    
    def oscillate(self, low: float, high: float, freq: float):
        """Generate sine wave values between low and high at the specified frequency."""
        pass

    def saveAsCSV(self):
        """Save the DataFrame to a CSV file."""
        sFilename = f'{self.name}.csv'
        self.log.info('Saving synthetic data to %s', sFilename)
        self.df.to_csv(sFilename)

    def plot(self):
        """Save a matplotlib plot of the generated dataframe."""
        ax = self.df.plot(kind='line', title=self.name)
        fig = ax.get_figure()
        sFilename = f'{self.name}.pdf'
        self.log.info('Saving plot as %s', sFilename)
        fig.savefig(sFilename)


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
    """
    A model generating high/low consumption values with random noise.
    Sampling rate is 15 minutes, so 96 values per day.
    Consumption varies from low to high depending on the day and hour.
    """

    def __init__(self, nValues: int, valLow: float, valHigh: float, dOptions: dict) -> None:
        """Constructor with low and high consumption values."""
        super().__init__('ConsumptionModel', nValues, dOptions)
        self.valLow  = valLow
        self.valHigh = valHigh

    def buildIndex(self):
        """Generate the dataframe index with 15 minute intervals."""
        return pd.date_range(start='01/01/2023', periods=self.nValues, freq='15min')

    def generate(self):
        self.log.info('Generating %d %s values', self.nValues, self.name)
        arrCons = []
        hourOpening = 7
        hourClosing = 19
        for i in range(self.nValues):
            hour    = self.df.index[i].hour
            weekday = self.df.index[i].dayofweek
            #self.log.info('Index is %s, day of week is %d, hour is %d', self.df.index[i], weekday, hour)
            if weekday == 6:
                # Sunday only has low consumption
                arrCons.append(self.valLow)
            elif hour == hourOpening:
                # Opening hour ramp-up
                min = self.df.index[i].minute
                arrCons.append(self.interpolate(self.valLow, self.valHigh, min/60.0))
            elif hour == hourClosing:
                # Closing hour ramp-down
                min = self.df.index[i].minute
                arrCons.append(self.interpolate(self.valHigh, self.valLow, min/60.0))
            elif hour > hourOpening and hour < hourClosing:
                # Open hours high consumption
                arrCons.append(self.valHigh)
            else:
                # Closed low consumption
                arrCons.append(self.valLow)
        return np.add(arrCons, self.noise(0.9))