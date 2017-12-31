#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""Provides the Farm class for the ants module.

The Farm object runs its own thread and continuously create ants according to initial parameters.
"""

import config
import uuid
import threading
import multiprocessing
import time
import logging
import ant
import utils

__author__ = "Doug Le Tough"
__copyright__ = "Copyright 2017, Doug Le Tough"
__credits__ = ["Doug Le Tough",]
__license__ = "WTFPL"
__version__ = "1.0.0"
__maintainer__ = "Doug Le Tough"
__email__ = "doug.letough@free.fr"
__status__ = "Testing"

###################################################################################################################
# Farm
###################################################################################################################

class Farm(threading.Thread):
  """ The Farm object continuously create ants untill it runs out of food.
  """
  def __init__(self, playground, display_q, position, growthrate, food, life, radius):
    """
    - playground: The Playground in which ants will be created
    - display_q: The FIFO queue in wich data are sent to the Display object
    - position: The Farm position as a tuple (x, y)
    - growthrate: The growthrate in ants/minute
    - food: The initial amount of food. One unit of food is needed for each ant creation.
    when the Farm runs out of food it will stay alive for <life> minutes. If ants store food
    in the Farm before the Farm runs out of <life>, then the ant creation process restart.
    - life: The number of minutes the Farm stay alive when all food has been consumed.
    - radius: The radius of the Farm. This is the display radius and the area where an ant is considered
    at home.
    """
    threading.Thread.__init__(self)
    self.ID = str(uuid.uuid4())
    self.playground = playground
    self.position = position
    self.growthrate = growthrate
    self.food = food
    self.life = life
    self.radius = radius
    self.display_q = display_q
    self.color = config.FARM_COLOR
    self.outline_color = config.FARM_OUTLINE_COLOR
    self.data = {'type': 'Farm %s' % (self.ID)}

  def __str__(self):
    """ Returns a string representation of the farm """
    return str(self.to_dict())

  def to_dict(self):
    """ Returns a dict representation of the Farm object. This representation is
    used by the Display workers to display the Farm.
    """
    return {'type': 'farm',
            'ID': self.ID,
            'position': self.position,
            'food': self.food,
            'life': self.life,
            'radius': self.radius,
            'color': self.color,
            'outline': self.outline_color}

  def run(self):
    """ The Farm object main thread loop """
    while self.life > 0:
      if self.food > 0:
        new_ant = ant.Ant(self.playground, self.display_q, self.position, self.ID)
        self.playground.add_ant(new_ant)
        new_ant.start()
        self.food -= 1
        logging.warning('\033[93mStatus:\033[0m Food: %d' % self.food, extra=self.data)
      else:
        self.life -= 1
        logging.warning('\033[91mDying:\033[0m Life: %d' % self.life, extra=self.data)
      time.sleep(60 / self.growthrate)
    logging.warning('\033[91mDead:\033[0m Life: %d' % self.life, extra=self.data)

  def in_range(self, position):
    """ Returns if wheter or not the given position is aside the Farm.
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

  def stop(self):
    """ Stops the Farm main loop. This will exit the Farm thread. """
    self.life = 0
