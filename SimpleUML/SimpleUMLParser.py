"""
A simple UML parser.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
import re
from enum import Enum
from SimpleUMLClass import *


class Mode(Enum):
    """Enumeration of parser mode."""
    Init    = 0
    Name    = 1
    Members = 2
    Methods = 3
    Done    = 4

    def __str__(self):
        return self.name
    

class SimpleUMLParser():
    """A simple UML parser."""
    log = logging.getLogger('SimpleUMLParser')

    def __init__(self, lang: str) -> None:
        """Constructor with language."""
        self.log.info('Constructor, language: %s', lang)
        self.lang = lang
        self.clazz: SimpleUMLClass

    def parseLine(self, line: str, mode: Mode):
        """Handle the specified line."""
        if mode == Mode.Name:
            self.log.info('Class name %s', line)
            self.clazz.setName(line)
        elif mode == Mode.Members:
            self.log.info('Member %s', line)
            match = re.match(r'-(.+): (.+)', line)
            if match:
                name = match.group(1)
                type = match.group(2)
                self.clazz.addMember(name, type)
            else:
                match = re.match(r'-(.+)', line)
                if match:
                    self.clazz.addMember(match.group(1), None)
        elif mode == Mode.Methods:
            self.log.info('Method %s', line)
            isPrivate = True
            params = []
            type = None
            if line.startswith('+'):
                isPrivate = False
            match1 = re.match(r'[-+](.+)\((.*)\): (.+)', line)
            match2 = re.match(r'[-+](.+)\((.*)\)', line)
            if match1:
                name = match1.group(1)
                sparams = match1.group(2)
                type = match1.group(3)
                #if len(sparams) > 0:
                #    params = sparams.split(', ')
                self.parseParams(sparams, params)
            elif match2:
                name = match2.group(1)
                sparams = match2.group(2)
                #if len(sparams) > 0:
                #    params = sparams.split(', ')
                self.parseParams(sparams, params)
            else:
                self.log.error('Failed to parse method from %s', line)
            
            self.log.info('Method %s has %d params:', name, len(params))
            for p in params:
                self.log.info('.. %s', p)
            self.clazz.addMethod(name, params, type, isPrivate)
        else:
            self.log.error('Unhandled mode %s for line %s', mode, line)

    def parseParams(self, line: str, result):
        """Parse method parameters from a comma-separated list."""
        if len(line) > 0:
            params = line.split(', ')
            for rawParam in params:
                if ': ' in rawParam:
                    parts = rawParam.split(': ')
                    result.append(SimpleUMLParam(parts[0], parts[1]))
                else:
                    result.append(SimpleUMLParam(rawParam))

    def parse(self, filename: str):
        """Parse the specified text file."""
        self.log.info('Parsing %s', filename)

        # Check input file exists
        if not os.path.exists(filename):
            self.log.error('File does not exist: %s', filename)
            return None
        
        # Create class object
        mode = Mode.Init
        if self.lang == 'cpp':
            self.clazz = SimpleUMLClassCpp()
        else:
            self.clazz = SimpleUMLClassPython()
        
        # Read file
        file = open(filename, 'r')
        for line in file.readlines():
            line = line.rstrip()
            if len(line) == 0:
                continue
            if len(line) == 0 or line.startswith('--'):
                mode = Mode(mode.value + 1)
                self.log.info('Parsing mode %s', mode.name)
                continue
            else:
                self.parseLine(line, mode)
        file.close()
        self.clazz.generate()
