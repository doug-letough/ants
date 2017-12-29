#!/usr/bin/python
# -*- coding:Utf-8 -*-

###################################################################################################################
# Ant
###################################################################################################################

import uuid
import threading
import multiprocessing
import random
import time
import logging
import utils

class Ant(threading.Thread):
  def __init__(self, playground, display_q, position, farm_id, speed=1):
    threading.Thread.__init__(self)
    self.ID = str(uuid.uuid4())
    self.playground = playground
    self.position = position
    self.display_q = display_q
    self.farm_id = farm_id
    self.speed = speed
    self.life = 10000
    self.max_history = 100
    self.history = {self.ID: []}
    self.food = 0
    self.color = utils.gen_color()

  def __str__(self):
    return str(self.to_dict())

  def to_dict(self):
    return {'type': 'ant', 
            'ID': self.ID,
            'position': self.position,
            'farm_id': self.farm_id,
            'life': self.life,
            'history': self.history[self.ID],
            'food': self.food
           }

  def walk(self):
    direction = utils.directions[int(random.random() * 9)]
    direction[0] = direction[0] * self.speed
    direction[1] = direction[1] * self.speed
    new_position = (self.position[0] + direction[0], self.position[1] + direction[1])
    self.display_q.put({'type': 'ant', 'ID': self.ID, 'old_position': self.position, 'new_position': new_position, 'color': self.color})
    self.position = new_position
    self.record()
    self.check_around()
    self.life -= 1
    time.sleep(.1)

  def record(self):
    self.history[self.ID].append(self.position)
    if len(self.history[self.ID]) > self.max_history:
      self.history[self.ID].pop(0)

  def check_around(self):
    around = self.playground.scan(self.position)
    ants = around['ants']
    farms = around['farms']
    mines = around['mines']
    if len(ants) > 0:
      for ant in ants:
        if ant.ID != self.ID:
          self.hail(ant)
    if len(farms) > 0:
      for farm in farms:
        self.check(farm)
    if len(mines) > 0:
      for mine in mines:
        self.mine(mine)

  def hail(self, ant):
    if ant.life > 0:
      data = {'type': 'Ant %s' % (self.ID)}
      logging.warning('\033[92mHail:\033[0m %s' % ant.ID, extra=data)
      self.history[ant.ID] = ant.history

  def check(self, farm):
    pass

  def mine(self, mine):
    if mine.stock > 0:
      data = {'type': 'Ant %s' % (self.ID)}
      logging.warning('\033[92mMine:\033[0m %s' % mine.ID, extra=data)
      self.food += 1

  def kill(self):
    self.life = 0

  def run(self):
    while self.life > 0:
      self.walk()
      data = {'type': 'Ant %s' % (self.ID)}
      logging.warning('\033[92mPosition:\033[0m %s, \033[92mLife:\033[0m %d, \033[92mFood:\033[0m %d, \033[92mHails:\033[0m %d' % (str(self.position), self.life, self.food, len(self.history)), extra=data)
    logging.warning('\033[91mDied at:\033[0m %s, \033[95mHistory:\033[0m %s' % (str(self.position), str([ant for ant in self.history])), extra=data)
