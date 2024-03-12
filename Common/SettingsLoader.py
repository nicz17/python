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

	def getSettingsDict(self):
		"""Get settings as a dict."""
		dict = {}
		if os.path.exists(self.filename):
			file = open(self.filename, 'r')
			dict = json.load(file)
			file.close()
		else:
			self.log.error('File does not exist: %s', self.filename)
		return dict

	def __str__(self):
		str = "SettingsLoader"
		str += f' from {self.filename}'
		return str


def testSettingsLoader():
	"""Unit test for SettingsLoader"""
	SettingsLoader.log.info("Testing SettingsLoader")
	obj = SettingsLoader('/home/nzw/SimpleUML/settings.json')
	obj.log.info(obj)
	dict = obj.getSettingsDict()
	obj.log.info(dict)

if __name__ == '__main__':
	logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
		level=logging.INFO, handlers=[logging.StreamHandler()])
	testSettingsLoader()

