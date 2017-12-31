#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""Provides the Mine class for the ants module.
"""

import config
import uuid
import utils
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
# Mine
###################################################################################################################

class Mine(object):
  """ The Mine object is the food source for ants."""
  def __init__(self, position, radius):
    """
    - position: The Mine position as a tuple (x, y)
    - radius: The mine radius. This is the display radius and the area where an ant is considered
    in range to pick up some food.
    """
    self.position = position
    self.radius = radius
    self.ID = str(uuid.uuid4())
    self.stock = config.MINE_INITIAL_STOCK
    self.color = config.MINE_COLOR
    self.outline_color = config.MINE_OUTLINE_COLOR
    self.data = {'type': 'Mine %s' % (self.ID)}

  def __str__(self):
    """ Returns the string representation of the Mine object"""
    return str(self.to_dict())
    
  def to_dict(self):
    """ Returns a dict representation of the Mine object. This representation is
    used by the Display workers to display the Mine.
    """
    return {'type': 'mine',
            'ID': self.ID,
            'position': self.position,
            'stock': self.stock,
            'color': self.color,
            'radius': self.radius,
            'outline': self.outline_color}

  def in_range(self, position):
    """ Returns if wheter or not the given position is aside the Mine.
    - Position: A tuple seen as coordinates (x, y)"""
    pos_x, pos_y = position
    dx = abs(pos_x - self.position[0])
    dy = abs(pos_y - self.position[1])
    result = False
    if dx + dy <= self.radius:
        result = True
    if dx > self.radius:
        result = False
    if dy > self.radius:
        result = False
    if pow(dx, 2) + pow(dy, 2) <= pow(self.radius, 2):
        result = True
    else:
      result = False
    return result

  def pick(self, q, ant_id):
    """ Remove <q> food unit from Mine stock
    - q: An int value"""
    self.stock -= q
    logging.warning('\033[92mAnt:\033[0m %s \033[92mmined:\033[0m %d, \033[92mLeft:\033[0m %d' % (ant_id, q, self.stock), extra=self.data)
    if self.stock == 0:
      logging.warning('\033[91mStock:\033[0m %d' % self.stock, extra=self.data)

  def stop(self):
    """ Actually do nothing"""
    logging.warning('\033[91mKilled\033[0m', extra=self.data)
