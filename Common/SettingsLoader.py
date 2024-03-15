"""
Module SettingsLoader:
Load settings options from a json file
and return them as a dict.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import json
import logging
import os

class SettingsLoader():
	"""Class SettingsLoader"""
	log = logging.getLogger("SettingsLoader")

	def __init__(self, filename: str):
		"""Constructor."""
		self.filename = filename
		self.dict = {}

	def loadSettings(self):
		"""Load the settings from the file."""
		if os.path.exists(self.filename):
			file = open(self.filename, 'r')
			self.dict = json.load(file)
			file.close()
		else:
			self.log.error('File does not exist: %s', self.filename)

	def getSettingsDict(self):
		"""Get settings as a dict."""
		return self.dict

	def __str__(self):
		str = "SettingsLoader"
		str += f' from {self.filename}'
		str += f' with {len(self.dict)} settings'
		return str


def testSettingsLoader():
	"""Unit test for SettingsLoader"""
	SettingsLoader.log.info("Testing SettingsLoader")
	loader = SettingsLoader('/home/nicz/prog/python/SimpleUML/settings.json')
	loader.loadSettings()
	loader.log.info(loader)
	dict = loader.getSettingsDict()
	loader.log.info(dict)

if __name__ == '__main__':
	logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
		level=logging.INFO, handlers=[logging.StreamHandler()])
	testSettingsLoader()

