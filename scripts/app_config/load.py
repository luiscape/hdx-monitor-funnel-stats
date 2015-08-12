#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

dir = os.path.split(os.path.realpath(__file__))[0]

def LoadConfig(type):
  '''Load configuration file.'''

  types = ['dev', 'prod']

  if type not in type:
    print '%s The configuration type `%s` does not exist.' % (">> ", type)
    return False
  
  try:
    j = os.path.join(dir, type + '.json')
    with open(j) as json_file:
      return json.load(json_file)

  except Exception as e:
    print "Could not load configuration."
    print e
    return False


if __name__ == '__main__':
  LoadConfig(type = 'dev')