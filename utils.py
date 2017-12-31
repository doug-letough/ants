#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""Provides common methods useful to the ants module.
"""

import random

__author__ = "Doug Le Tough"
__copyright__ = "Copyright 2017, Doug Le Tough"
__credits__ = ["Doug Le Tough",]
__license__ = "WTFPL"
__version__ = "1.0.0"
__maintainer__ = "Doug Le Tough"
__email__ = "doug.letough@free.fr"
__status__ = "Testing"
###################################################################################################################
# Utils
###################################################################################################################

directions = { 0: [0, 0],
               1: [1, 0],
               2: [-1, 0],
               3: [0, -1],
               4: [0, 1],
               5: [-1, 1],
               6: [1, 1],
               7: [1, -1],
               8: [-1, -1]
             }

def random_dir():
  """ Randomly returns one of the direction values.
  Directions values are: -1, 0, 1
  """
  directions = [-1, 0, 1]
  return directions[int(random.random() * len(directions))]

def gen_color():
  """ Returns a randomly generated hexadecimal color value (HTML style)."""
  alpha = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')
  return '#%s' % ''.join([random.choice(alpha) for _ in range(6)])
