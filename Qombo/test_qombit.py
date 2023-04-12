"""
Unit test for Qombit class.
"""

import unittest
from Qombit import *
from QombitFactory import *

class TestQombit(unittest.TestCase):
    def setUp(self):
        self.gen   = QombitFactory.fromValues('Gen', OrKind.Generator, 1, OrRarity.Common)
        self.basic = QombitFactory.fromValues('Bas', OrKind.Spiral, 1, OrRarity.Common)
        self.star9 = QombitFactory.fromValues('Star', OrKind.Star, 9, OrRarity.Common)
        self.obj   = QombitFactory.createObjective(1, 1)

    def test_canGenerate(self):
        """Test qombit generation."""
        self.assertTrue(self.gen.canGenerate(), 'Expect generator can generate')
        self.assertFalse(self.basic.canGenerate(), 'Expect basic cannot generate')
        self.assertTrue(self.star9.canGenerate(), 'Expect lvl9 can generate')
        self.assertFalse(self.obj.canGenerate(), 'Expect objective cannot generate')

    def test_canSell(self):
        """Test qombit selling."""
        self.assertFalse(self.gen.canSell(), 'Expect generator cannot be sold')
        self.assertTrue(self.basic.canSell(), 'Expect basic can be sold')
        self.assertFalse(self.star9.canSell(), 'Expect lvl9 cannot be sold')
        self.assertFalse(self.obj.canSell(), 'Expect objective cannot be sold')

    def test_canEvolve(self):
        """Test qombit evolution."""
        self.assertTrue(self.gen.canEvolve(), 'Expect generator can evolve')
        self.assertTrue(self.basic.canEvolve(), 'Expect basic can evolve')
        self.assertFalse(self.star9.canEvolve(), 'Expect lvl9 cannot evolve')
        self.assertFalse(self.obj.canEvolve(), 'Expect objective cannot evolve')

    def test_evolve(self):
        """Test qombit evolution."""
        lvl1 = QombitFactory.fromValues('Star', OrKind.Star, 1, OrRarity.Common)
        lvl2 = QombitFactory.fromValues('Star', OrKind.Star, 2, OrRarity.Common)
        self.assertNotEqual(lvl1, lvl2, 'Expect lvl1 and lvl2 different')
        self.assertTrue(lvl1.canEvolve(), 'Expect lvl1 can evolve')
        lvl1.evolve()
        #print(f'Level 1 evolved into {lvl1}')
        self.assertEqual(lvl1, lvl2, 'Expect lvl1 evolved into lvl2')

    def test_json(self):
        """Test qombit to json and back."""
        json = self.basic.toJson()
        self.assertIsNotNone(json, 'Expect json data')
        recon = QombitFactory.fromJson(json)
        self.assertEqual(self.basic, recon, 'Expect accurate json reconstruction')
    

if __name__ == '__main__':
    unittest.main()
