#!/usr/bin/python
# -*- coding:Utf-8 -*-

###################################################################################################################
# Farm
###################################################################################################################

import uuid
import threading
import multiprocessing
import time
import logging
import ant

class Farm(threading.Thread):
  def __init__(self, playground, display_q, position, growthrate, food, life):
    threading.Thread.__init__(self)
    self.ID = str(uuid.uuid4())
    self.playground = playground
    self.position = position
    self.growthrate = growthrate
    self.food = food
    self.life = life
    self.display_q = display_q

  def __str__(self):
    return str(self.to_dict())

  def to_dict(self):
    return {'type': 'farm', 'ID': self.ID, 'position': self.position, 'food': self.food, 'life': self.life}

  def run(self):
    data = {'type': 'Farm %s' % (self.ID)}
    while self.life > 0:
      if self.food > 0:
        new_ant = ant.Ant(self.playground, self.display_q, self.position, self.ID)
        self.playground.add_ant(new_ant)
        new_ant.start()
        self.food -= 1
        logging.warning('\033[93mStatus:\033[0m Food: %d' % self.food, extra=data)
      else:
        self.life -= 1
        logging.warning('\033[91mDying:\033[0m Life: %d' % self.life, extra=data)
      time.sleep(60 / self.growthrate)
    self.stop()

  def stop(self):
    data = {'type': 'Farm %s' % (self.ID)}
    logging.warning('\033[91mDead:\033[0m Life: %d' % self.life, extra=data)
    self.life = 0
