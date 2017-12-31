#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""Provides the Ant class for the ants module.
"""

import config
import uuid
import threading
import multiprocessing
import random
import time
import logging
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
# Ant
###################################################################################################################

class Ant(threading.Thread):
  """ The Ant object is a self living virtual creature that tries to simulate
  some ant's basic behaviour.
  The Ant object runs its own thread.
  """
  def __init__(self, playground, display_q, position, farm_id):
    """
    - playground: The Playground in which the Ant lives
    - display_q: The FIFO queue in wich data are sent to the Display object
    - position: A tuple seen as initial position (x, y)
    - farm_id: The Farm ID to which the Ant belongs
    """
    threading.Thread.__init__(self)
    self.color = config.ANT_HUNTING_COLOR
    self.outline_color = config.ANT_NEUTRAL_OUTLINE_COLOR
    self.ID = str(uuid.uuid4())
    self.radius = config.ANT_RADIUS
    self.playground = playground
    self.position = position
    self.new_position = position
    self.direction = None
    self.display_q = display_q
    self.farm_id = farm_id
    self.max_life = config.ANT_MAX_LIFE
    self.life = self.max_life
    self.max_history = config.ANT_MAX_HISTORY
    self.history = []
    self.togo = []
    self.max_food = config.ANT_MAX_FOOD
    self.food = 0
    self.data = {'type': 'Ant %s' % (self.ID)}

  def __str__(self):
    """ Returns a string representation of the Ant. """
    return str(self.to_dict())

  def to_dict(self):
    """ Returns a dict representation of the Ant object. This representation is
    used by the Display workers to display the Ant.
    """
    return {'type': 'ant',
            'ID': self.ID,
            'old_position': self.position,
            'new_position': self.new_position,
            'radius': self.radius,
            'color': self.color,
            'outline': self.outline_color
           }

  def set_colors(self):
    """ Adjust the Ant colors depending on the Ant status.
    """
    if self.food > 0:
      self.color = config.ANT_HOMING_COLOR
      self.outline_color = config.ANT_LOST_OUTLINE_COLOR
      if self.is_busy():
        self.outline_color = config.ANT_BUSY_OUTLINE_COLOR
    else:
      self.color = config.ANT_HUNTING_COLOR
      self.outline_color = config.ANT_NEUTRAL_OUTLINE_COLOR
      if self.is_busy():
        self.outline_color = config.ANT_BUSY_OUTLINE_COLOR

  def walk(self):
    """ Set a new position.
    If Ant already has a path to go, then the next position is picked up from this path.
    Otherwise, a new position is randomly picked up. 
    """
    if self.is_busy():
      self.new_position = self.pop_new_position()
    else:
      self.new_position = self.set_new_position()
    self.display_q.put(self.to_dict())
    self.position = self.new_position
    
  def set_new_position(self):
    """ Set a new position from the actual position.
    A new position is randomly generated by adding -1, 0 or 1 to one of
    the actual position componant (x or y).
    If the new position is out of the playground then the position is
    adjusted. Thus an ant can not walk out of the play ground which is finite.
    """
    if not self.direction:
      self.direction = (utils.random_dir(), utils.random_dir())
    else:
      if not int(random.random() * 10) % 4:
        if int(random.random() * 2) % 2:
          self.direction = (utils.random_dir(), self.direction[1])
        else:
          self.direction = (self.direction[0], utils.random_dir())
    new_pos_x = self.position[0] + self.direction[0]
    new_pos_y = self.position[1] + self.direction[1]
    if new_pos_x > self.playground.width:
      new_pos_x = self.playground.width
    if new_pos_x < 0:
      new_pos_x = 0
    if new_pos_y > self.playground.height:
      new_pos_y = self.playground.height
    if new_pos_y < 0:
      new_pos_y = 0
    return (new_pos_x, new_pos_y)

  def pop_new_position(self):
    """ Pick the next position in the path to go.
    """
    return self.togo.pop(0)

  def record(self):
    """ Record the actual position in the Ant history.
    For each new record, the history is recreated in a way that the shortest path
    from the oldest position to the current position is retained.
    Still, the new shortest path will only use position wihin the history.
    The shortest path from within the history is not always (never ?) the shortest path on the play ground.
    """
    if len(self.history) == 0:
      self.history.append(self.position)
      return
    x, y = self.position
    new_history = []
    for position in self.history:
      px, py = position
      new_history.append(position)
      if abs(px - self.position[0]) <= 1 and abs(py - self.position[1]) <=1:
        new_history.append(self.position)
        self.history = new_history[:]
        return
    logging.warning("\033[91mWTF:\033[0m %s, \033[92mHistory:\033[0m %d" % (str(self.position), len(self.history)) , extra=self.data)

  def clean_history(self):
    """ Delete oldest position in history when history length is larger than <max_history>.
    See config.ANT_MAX_HISTORY
    """
    if len(self.history) > self.max_history:
      logging.warning("\033[92mCleaning history:\033[0m %d" % len(self.history), extra=self.data)
      self.history.pop(0)

  def check_around(self):
    """ Process actions according to what is around the present position.
    Object around the present position are given bay the Playground.scan(position) method.
    """
    around = self.playground.scan(self.position)
    ants = around['ants']
    farms = around['farms']
    mines = around['mines']
    if len(farms) > 0:
      for farm in farms:
        self.store(farm)
    if len(mines) > 0:
      for mine in mines:
        self.mine(mine)
    if len(ants) > 0:
      for ant in ants:
        if ant.ID != self.ID:
          self.hail(ant)

  def hail(self, ant):
    """ Hails the given Ant.
    Whenever an Ant encounter an another, it hails it.
    Depending on the status of each the concerned Ants, some data are exchanged.
    An Ant can not hail a dead Ant.
    """ 
    todo = "\033[92mHail:\033[0m %s " % ant.ID
    if not self.is_busy():
      if ant.life > 0:
        if ant.food > 0 and self.food == 0:
          # Ant is lost, so we tell it the path to home
          self.togo = [ant.position] + list(reversed(ant.history))
          todo += '\033[92mFood path:\033[0m %s, \033[92mAnt position:\033[0m %s' % (str(self.togo), str(ant.position))
          self.wait(config.ANT_SLEEP_DELAY)
        elif ant.food == 0 and self.food > 0:
          # Ant is lost, we tell it the pass to food
          self.togo = [ant.position] + list(reversed(ant.history))
          todo += '\033[92mHome path:\033[0m %s, \033[92mAnt position:\033[0m %s' % (str(self.togo), str(ant.position))
          self.wait(config.ANT_SLEEP_DELAY)
        elif ant.is_busy() and ant.food == 0 and self.food == 0 and not self.is_busy():
          # Were are lost and ant seems to know the path to food
          self.togo = ant.togo[:]
          self.history = ant.history[:]
          todo += '\033[92mFood path:\033[0m %s, \033[92mAnt position:\033[0m %s' % (str(self.togo), str(ant.position))
          self.wait(config.ANT_SLEEP_DELAY)
        elif ant.is_busy() and ant.food > 0 and self.food > 0 and not self.is_busy():
          # We are lost and ant seems to know the path to home
          self.togo = ant.togo[:]
          self.history = ant.history[:]
          todo += '\033[92mHome path:\033[0m %s, \033[92mAnt position:\033[0m %s' % (str(self.togo), str(ant.position))
          self.wait(config.ANT_SLEEP_DELAY)
    logging.warning(todo, extra=self.data)

  def store(self, farm):
    """ Stores the carried food to the given farm. """
    if farm.ID == self.farm_id and self.food > 0:
      food = self.food
      farm.food += self.food
      self.food = 0
      self.swap_histories()
      logging.warning("\033[92mFood stored:\033[0m %d, \033[92mTotal stock:\033[0m %s" % (food, farm.food), extra=self.data)
      logging.warning("\033[92mFood path:\033[0m %s" % str(self.togo), extra=self.data)

  def mine(self, mine):
    """ Pick the maximum food amount from the given mine."""
    if self.food < self.max_food:
      food = 0
      if mine.stock > 0:
        food = mine.stock
        self.swap_histories()
        if mine.stock >= self.max_food - self.food:
          food = self.max_food - self.food
      mine.pick(food, self.ID)
      self.food = food
      logging.warning('\033[92mHome path:\033[0m %s' % str(self.togo), extra=self.data)

  def swap_histories(self):
    """ Swap history and path to go.
    When an Ant find food, it needs to go back home.
    The partial or complete path to home is in its history so the history is reverted then given has a path to go.
    Once the path to go is set, the actual history is wiped out.
    Same process occurs when an Ant comes back to home with food, so it can go back to the Mine.
    
    """
    self.togo = list(reversed(self.history))
    self.history = [self.position]
    logging.warning('\033[92mHistory:\033[0m %s, \033[92mTogo:\033[0m %s' % (str(self.history), str(self.togo)), extra=self.data)

  def in_range(self, position):
    """ Returns if wheter or not the given position is aside the Ant.
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

  def is_busy(self):
    """ Returns wheter or not the Ant is busy.
    An Ant is busy when the length of its path to go is > 0.
    """
    return len(self.togo) > 0

  def wait(self, delay):
    """ Wait time seconds """
    time.sleep(delay)

  def stop(self):
    """ Kill the Ant.
    this will exit the Ant thread. """
    self.life = 0

  def run(self):
    """ The Ant thread main loop """
    while self.life > 0:
      self.check_around()
      self.set_colors()
      self.walk()
      self.record()
      self.clean_history()
      self.life -= 1
      if self.life == 0 and self.food > 0:
        self.food -= 1
        self.life += int(self.max_life / 3)
      logging.warning('\033[92mPosition:\033[0m %s, \033[92mLife:\033[0m %d, \033[92mFood:\033[0m %d, \033[92mHistory:\033[0m %d' % (str(self.position), self.life, self.food, len(self.history)), extra=self.data)
      time.sleep(.1)
    logging.warning('\033[91mDied at:\033[0m %s, \033[95mHistory:\033[0m %d' % (str(self.position), len(self.history)), extra=self.data)
