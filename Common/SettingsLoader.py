"""
Module SettingsLoader:
Load settings options from a json file
and return them as a dict.
This is a singleton.
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
	_instance = None

	def __new__(cls, filename: str):
		"""Create a singleton object."""
		if cls._instance is None:
			cls._instance = super(SettingsLoader, cls).__new__(cls)
			cls._instance.log.info('Created the SettingsLoader singleton from %s', filename)
			# Put any initialization here.
			cls._instance.filename = filename
			cls._instance.dict = {}
		return cls._instance

	def __init__(self, filename: str):
		"""Constructor. Unused as all is done in new."""
		pass

	def loadSettings(self) -> None:
		"""Load the settings from the file."""
		self.log.info('Loading settings from %s', self.filename)
		if os.path.exists(self.filename):
			file = open(self.filename, 'r')
			self.dict = json.load(file)
			file.close()
		else:
			self.log.error('File does not exist: %s', self.filename)

	def getSettingsDict(self) -> dict:
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

	loader2 = SettingsLoader('blam')
	loader2.log.info(loader2)

if __name__ == '__main__':
	logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
		level=logging.INFO, handlers=[logging.StreamHandler()])
	testSettingsLoader()

