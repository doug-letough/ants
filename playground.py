#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""Provides the Playground class which is the sandbox where
ants are living.
"""

import threading
import multiprocessing
import Queue
import utils
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
# Playground
###################################################################################################################


class Worker(threading.Thread):
  """ The Worker object provides a way to process data found in a queue.
      When data is found, the corresponding object is killed.

      The Worker object runs in its own thread.
  """
  def __init__(self, ants, farms, mines, queue):
    """
    ants: The ant collection
    farms: The farm collection
    mines: The mine collection
    queue: The FIFO queue where the data have to be collected
    """
    threading.Thread.__init__(self)
    self.ants = ants
    self.mines = mines
    self.farms = farms
    self.queue = queue
    self.active = True
    self.data = {'type': 'Playground worker'}

  def run(self):
    """
    The Worker thread main loop:
    - Get data from queue and give it to the process method
    """
    logging.warning('\033[93mReport status:\033[0m \033[92mActive:\033[0m %s' % self.active, extra=self.data)
    while self.active:
      item = self.queue.get()
      self.process(item)
    logging.warning('\033[93mReport status:\033[0m \033[92mActive:\033[0m %s' % self.active, extra=self.data)

  def process(self, item):
    """
    Displays received item.
    Item must be a dict (JSON like hash)
    Valid data can be one of the 3 following type:
    - ant
    - farm
    - mine
    """
    if item['type'] == 'kill':
      logging.warning('\033[93mKill signal:\033[0m Received', extra=self.data)
      for farm in self.farms:
        self.farms[farm].stop()
      for mine in self.mines:
        self.mines[mine].stop()
      for ant in self.ants:
        self.ants[ant].stop()
    self.stop()

  def stop(self):
    """
    Exit from main loop
    """
    self.active = False


class Playground(object):
  """ The Playground class provides the eco-system within ants are living.
  - size is a tuple seen as a dimension (width, height).
  """
  def __init__(self, size, response_q):
    self.width, self.height = size
    self.response_q = response_q
    self.ants = {}
    self.farms = {}
    self.mines = {}
    self.worker = Worker(self.ants, self.farms, self.mines, self.response_q)
    self.worker.start()
    self.data = {'type': 'Playground'}

  def scan(self, position):
    """ Returns all objects (ants, farms, mines) nearby the given position.
    - position is a tupe seen as coordinates (x, y)
    """
    try:
      ants = [self.ants[ant] for ant in self.ants if self.ants[ant].in_range(position) and self.ants[ant].is_alive()]
      farms = [self.farms[farm] for farm in self.farms if self.farms[farm].in_range(position)]
      mines = [self.mines[mine] for mine in self.mines if self.mines[mine].in_range(position)]
    except RuntimeError:
      return self.scan(position)
    return {'ants': ants, 'farms': farms, 'mines': mines}

  def add_ant(self, ant):
    """ Add ant to the playground ant collection """
    logging.warning('\033[93mAdd ant:\033[0m %s, \033[92mPosition:\033[0m %s' % (ant.ID, ant.position), extra=self.data)
    self.ants[ant.ID] = ant

  def add_farm(self, farm):
    """ Add farm to the playground farm collection """
    logging.warning('\033[93mAdd farm:\033[0m %s, \033[92mPosition:\033[0m %s' % (farm.ID, farm.position), extra=self.data)
    self.farms[farm.ID] = farm

  def add_mine(self, mine):
    """ Add mine to the playground mine collection """
    logging.warning('\033[93mAdd mine:\033[0m %s, \033[92mPosition:\033[0m %s' % (mine.ID, mine.position), extra=self.data)
    self.mines[mine.ID] = mine

  def get_ant(self, ant_id):
    """ Returns the ant which ID is given.
    Returns None if no ant in the ant collection has the given ID"""
    try:
      return self.ants[ant_id]
    except IndexError:
      return None

  def get_farm(self, farm_id):
    """ Returns the farm which ID is given.
    Returns None if no farm in the farm collection has the given ID"""
    try:
      return self.farms[farm_id]
    except IndexError:
      return None

  def get_mine(self, mine_id):
    """ Returns the mine which ID is given.
    Returns None if no mine in the mine collection has the given ID"""
    try:
      return self.mines[mine_id]
    except IndexError:
      return None
