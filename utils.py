#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""Provides common methods useful to the ants module.
"""

import random
import logging

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

data = {'type': 'Utils:'}

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

def get_shortest_path(ant_ID, checkpoints, destination, max_distance):
  """ Returns shortest path to destination from within points in checkpoints """
  best_path = []
  if len(checkpoints) == 0:
    # This the first point ever for this ant
    # So we just add it and return the list as is
    checkpoints.append(destination)
    return checkpoints
  # Get the index of all points in checkpoints in relation to <destination>
  # and keep only the first one
  try:
    best = [checkpoints.index(point) for point in checkpoints if in_range(point, destination, max_distance)][0]
  except IndexError:
    logging.warning('\033[91m[get_shortest_path]:\033[0m \033[92mAnt ID:\033[0m %s, \033[92mCheckpoints:\033[0m %s, \033[92mdestination:\033[0m %s' % (ant_ID, str(checkpoints), str(destination)), extra=data)
  # Best path is the part of checkpoints from 0 to the index of the first
  # point in range of <destination>
  best_path = checkpoints[:best+1]
  if best_path[len(best_path) - 1] != destination:
    # destination is not already in best path, so we add it
    best_path.append(destination)
  return best_path

def in_range(point_a, point_b, max_distance):
  """ Returns if wether or not 2 points (x, y) are separated from <distance> at max.
  This is very different from Ant.in_range(), Farm.in_range() or Mine.in_range() which return
  if a point is inside a perimeter.
  """
  return abs(point_a[0] - point_b[0]) <= max_distance and abs(point_a[1] - point_b[1]) <= max_distance
