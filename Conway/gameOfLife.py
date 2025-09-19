"""Module gameOfLife"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import json
import logging
import numpy as np
import os
import random


class State():
    """A State in the game of life."""
    log = logging.getLogger("State")

    def __init__(self, lines):
        """Constructor."""
        self.lines = lines
        self.w = len(self.lines[0])
        self.h = len(self.lines)

    def getCell(self, x: int, y: int) -> int:
        return self.lines[y % self.h][x % self.w]

    def countNeighbors(self, x: int, y: int) -> int:
        """Count live neighbors of the cell at x, y."""
        count = 0
        for xi in [x-1, x, x+1]:
            for yi in [y-1, y, y+1]:
                if not (xi==x and yi==y):
                    count += self.getCell(xi, yi)
        return count

    def countAlive(self) -> int:
        """Count alive cells in this state."""
        count = 0
        for x in range(self.w):
            for y in range(self.h):
                count += self.getCell(x, y)
        return count
    
    def getSize(self):
        """Get the state size as (width, height)."""
        return (self.w, self.h)

    def toJson(self):
        """Create a dict of this State for json export."""
        data = []
        for line in self.lines:
            data.append(''.join(str(i) for i in line))
        return data

    def __str__(self):
        s = f'State [{self.w},{self.h}]\n'
        for line in self.lines:
            s += ''.join(str(i) for i in line) + '\n'
        return s


class SeedGenerator():
    """Factory to generate seed states."""
    log = logging.getLogger("SeedGenerator")

    def __init__(self, size):
        """Constructor."""
        self.size = size
        self.log.info(f'Constructor with size {size}')

    def random(self, density: float) -> State:
        """Create a new random seed."""
        lines = []
        for y in range(self.size[1]):
            line = []
            for x in range(self.size[0]):
                val = 1 if random.random() < density else 0
                line.append(val)
            lines.append(line)
        return State(lines)

    def fromFile(self, filename: str) -> State:
        """New seed from file."""
        if not os.path.exists(filename):
            self.log.error(f'File not found: {filename}')
            return None
        cells = []
        with open(filename, 'r') as file:
            data = json.load(file)
            for line in data['seed']:
                cells.append([int(s) for s in list(line)])
        return State(cells)

    def blank(self) -> State:
        """Create a new blank state."""
        lines = []
        for y in range(self.size[1]):
            line = []
            for x in range(self.size[0]):
                line.append(0)
            lines.append(line)
        return State(lines)


class GameOfLife():
    """Class GameOfLife"""
    log = logging.getLogger("GameOfLife")

    def __init__(self, id: str, seed: State):
        """Constructor."""
        self.id = id
        self.size = seed.getSize()
        self.seed  = seed
        self.state = seed

    def run(self, ticks: int):
        """Run the game for a number of ticks."""
        self.log.info(self.state)
        for tick in range(ticks):
            nAlive = self.state.countAlive()
            self.log.info(f'Tick {tick}: {nAlive} alive')
            self.log.info(self.state)
            if nAlive == 0:
                self.log.info('Dead')
                return
            else:
                self.evolve()
        self.log.info(self.state)

    def setSeed(self, seed: State):
        """Set the seed state."""
        self.seed  = seed
        self.state = seed
        
    def evolve(self):
        """Evolve the state."""
        state = self.newStateBlank()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                state.lines[y][x] = self.getNextValue(x, y)
        self.state = state

    def getNextValue(self, x: int, y: int) -> int:
        """Get next cell value."""
        val = self.getState().getCell(x, y)
        cn  = self.getState().countNeighbors(x, y)
        if val == 0:
            if cn == 3: return 1
        if val == 1:
            if cn < 2: return 0
            if cn > 3: return 0
        return val
    
    def findLongevity(self, maxTicks: int) -> int:
        """Find the number of ticks until the game ends."""
        self.state = self.seed
        for tick in range(maxTicks):
            nAlive = self.state.countAlive()
            if nAlive == 0:
                return tick
            else:
                self.evolve()
        return maxTicks
    
    def findVariance(self, maxTicks: int) -> float:
        """Find the variance of the number of alive cells."""
        self.state = self.seed
        counts = []
        for tick in range(maxTicks):
            nAlive = self.state.countAlive()
            counts.append(nAlive)
            if nAlive == 0:
                break
            else:
                self.evolve()
        return np.var(counts)

    def findPeriod(self) -> int:
        """Find period."""
        # TODO: implement period detection
        pass

    def newStateBlank(self) -> State:
        """Create a new blank state."""
        lines = []
        for y in range(self.size[1]):
            line = []
            for x in range(self.size[0]):
                line.append(0)
            lines.append(line)
        return State(lines)

    def getState(self) -> State:
        return self.state

    def getSize(self):
        """Getter for size"""
        return self.size

    def toJson(self):
        """Create a dict of this GameOfLife for json export."""
        data = {
            'id': self.id,
            'size': self.size,
            'seed': self.seed.toJson()
        }
        return data
    
    def toJsonFile(self):
        """Save as json file."""
        filename = f'{self.id}.json'
        with open(filename, 'w') as file:
            file.write(json.dumps(self.toJson(), indent=2))

    def __str__(self):
        return f'GameOfLife {self.id} {self.size}'


def testState():
    """Unit test for State"""
    State.log.info("Testing State")
    block   = [[0,0,0,0,0], [0,1,1,0,0], [0,1,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]
    blinker = [[0,0,0,0,0], [0,0,0,0,0], [0,1,1,1,0], [0,0,0,0,0], [0,0,0,0,0]]
    state = State(blinker)
    state.log.info(state)
    state.log.info(state.toJson())

def testSeedGenerator():
    """Unit test for SeedGenerator."""
    gen = SeedGenerator([5, 5])
    seed = gen.fromFile('glider.json')
    gen.log.info(seed)

def testGameOfLife():
    """Unit test for GameOfLife"""
    GameOfLife.log.info("Testing GameOfLife")
    size = (15, 10)
    density = 0.15
    gen = SeedGenerator(size)
    #game = GameOfLife('TestGame', gen.blank())
    game = GameOfLife('TestGame', gen.random(density))
    #game = GameOfLife('TestGame', gen.fromFile('glider.json'))
    #blinker = [[0,0,0,0,0], [0,0,0,0,0], [0,1,1,1,0], [0,0,0,0,0], [0,0,0,0,0]]
    game.log.info(game)
    game.toJsonFile()
    game.run(20)
    longevity = game.findLongevity(1000)
    variance  = game.findVariance(100)
    game.log.info(f'Longevity: {longevity} ticks, variance: {variance}')

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    #testState()
    #testSeedGenerator()
    testGameOfLife()
