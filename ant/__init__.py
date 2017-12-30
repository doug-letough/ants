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
  def __init__(self, radius, playground, display_q, position, farm_id, speed=1):
    threading.Thread.__init__(self)
    self.hunting_color = '#FF0000'
    self.homing_color = '#00FF00'
    self.normal_outline_color = '#FFFFFF'
    self.busy_outline_color = '#0000FF'
    self.outline_color = self.normal_outline_color
    self.ID = str(uuid.uuid4())
    self.radius = radius
    self.playground = playground
    self.position = position
    self.new_position = position
    self.display_q = display_q
    self.farm_id = farm_id
    self.speed = speed
    self.max_life = 10000
    self.life = self.max_life
    self.max_history = self.max_life
    self.history = []
    self.togo = []
    self.max_food = 5
    self.food = 0
    self.color = self.hunting_color
    self.data = {'type': 'Ant %s' % (self.ID)}

  def __str__(self):
    return str(self.to_dict())

  def to_dict(self):
    return {'type': 'ant',
            'ID': self.ID,
            'old_position': self.position,
            'new_position': self.new_position,
            'radius': self.radius,
            'color': self.color,
            'outline': self.outline_color
           }

  def walk(self):
    if len(self.togo) > 0:
      self.new_position = self.pop_new_position()
      self.outline_color = self.busy_outline_color
    else:
      self.outline_color = self.normal_outline_color
      self.new_position = self.set_new_position()
    self.display_q.put(self.to_dict())
    self.position = self.new_position
    
  def set_new_position(self):
    direction = utils.directions[int(random.random() * len(utils.directions))]
    if int(random.random() * 2) % 2:
      direction[0] = direction[0] * self.speed
    else:
      direction[1] = direction[1] * self.speed
    return (self.position[0] + direction[0], self.position[1] + direction[1])

  def pop_new_position(self):
    new_pos = self.togo.pop(0)
    if new_pos == self.position:
      return self.set_new_position()
    return new_pos

  def record(self):
    if len(self.history) == 0:
      self.history.append(self.position)
      return
    x, y = self.position
    new_history = []
    for position in self.history:
      px, py = position
      new_history.append(position)
      if (x == px and y == py+1) or \
         (x == px and y == py-1) or \
         (x == px+1 and y == py) or \
         (x == px-1 and y == py) or \
         (x == px+1 and y == py+1) or \
         (x == px+1 and y == py-1) or \
         (x == px-1 and y == py+1) or \
         (x == px-1 and y == py-1):
        new_history.append(self.position)
        self.history = new_history[:]
        return

  def clean_history(self):
    if len(self.history) > self.max_history:
      self.history.pop(0)

  def check_around(self):
    around = self.playground.scan(self.position)
    ants = around['ants']
    farms = around['farms']
    mines = around['mines']
    if len(farms) > 0:
      for farm in farms:
        self.check(farm)
    if len(mines) > 0:
      for mine in mines:
        self.mine(mine)
    if len(ants) > 0:
      for ant in ants:
        if ant.ID != self.ID:
          self.hail(ant)

  def hail(self, ant):
    todo = "\033[92mHail:\033[0m %s" % ant.ID
    if len(self.togo) == 0:
      if ant.life > 0:
        if ant.food > 0:
          if self.food == 0:
            self.togo = list(reversed(ant.history))
            todo += ' New food path is set'
        elif ant.food == 0:
          if self.food > 0:
            self.togo = list(reversed(ant.history))
            todo += ' New home path is set'
    logging.warning(todo, extra=self.data)

  def check(self, farm):
    if farm.ID == self.farm_id and self.food > 0:
      food = self.food
      farm.food += self.food
      self.food = 0
      self.color = self.hunting_color
      self.togo = list(reversed(self.history))
      logging.warning("Food stored: %d" % food, extra=self.data)
      logging.warning("New food path is set: %s" % str(self.togo), extra=self.data)

  def mine(self, mine):
    if self.food < self.max_food:
      food = 0
      if mine.stock >= self.max_food - self.food:
        food = self.max_food - self.food
        self.color = self.homing_color
        self.togo = list(reversed(self.history))
      elif mine.stock > 0:
        food = mine.stock
        self.color = self.homing_color
        self.togo = list(reversed(self.history))
      mine.stock -= food
      self.food = food
      logging.warning('\033[92mMined from %s:\033[0m Food: %d' % (mine.ID, food), extra=self.data)
      logging.warning('\033[92mTogo:\033[0m %s' % str(self.togo), extra=self.data)

  def in_range(self, position):
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

  def kill(self):
    self.life = 0

  def run(self):
    while self.life > 0:
      self.check_around()
      self.walk()
      self.record()
      self.clean_history()
      self.life -= 1
      if self.life == 0 and self.food > 0:
        self.food -= 1
        self.life += int(self.max_life / 3)
      logging.warning('\033[92mPosition:\033[0m %s, \033[92mLife:\033[0m %d, \033[92mFood:\033[0m %d' % (str(self.position), self.life, self.food), extra=self.data)
      time.sleep(.1)
    logging.warning('\033[91mDied at:\033[0m %s, \033[95mHistory:\033[0m %s' % (str(self.position), str([ant for ant in self.history])), extra=self.data)
