#!/usr/bin/python
# -*- coding:Utf-8 -*-

###################################################################################################################
# Playground
###################################################################################################################

import threading
import multiprocessing
import Queue
import utils
import logging

class Playground(object):
  def __init__(self, size):
    self.width, self.height = size
    self.ants = {}
    self.farms = {}
    self.mines = {}

  def scan(self, position):
    try:
      around = [(utils.directions[direction][0] + position[0], utils.directions[direction][1] + position[1]) \
                for direction in utils.directions]
      ants = [self.ants[ant] for ant in self.ants if self.ants[ant].position == position]
      farms = [self.farms[farm] for farm in self.farms if self.farms[farm].position == position]
      mines = [self.mines[mine] for mine in self.mines if self.mines[mine].position == position]
    except RuntimeError:
      return self.scan(position)
    return {'ants': ants, 'farms': farms, 'mines': mines}

  def add_ant(self, ant):
    data = {'type': 'Playground'}
    logging.warning('\033[93mAdd ant:\033[0m %s' % ant.ID, extra=data)
    self.ants[ant.ID] = ant

  def add_farm(self, farm):
    data = {'type': 'Playground'}
    logging.warning('\033[93mAdd farm:\033[0m %s' % farm.ID, extra=data)
    self.farms[farm.ID] = farm

  def add_mine(self, mine):
    data = {'type': 'Playground'}
    logging.warning('\033[93mAdd mine:\033[0m %s' % mine.ID, extra=data)
    self.mines[mine.ID] = mine

  def get_ant(self, ant_id):
    return self.ants[ant_id]

  def get_farm(self, farm_id):
    return self.farms[farm_id]

  def get_mine(self, mine_id):
    return self.mines[mine_id]
