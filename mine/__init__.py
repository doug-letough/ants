#!/usr/bin/python
# -*- coding:Utf-8 -*-

###################################################################################################################
# Mine
###################################################################################################################

import uuid
import utils
import random
import logging

class Mine(object):
  def __init__(self, position, radius):
    self.position = position
    self.radius = radius
    self.ID = str(uuid.uuid4())
    self.stock = 1000
    self.color = utils.gen_color()
    self.outline_color = '#FFFFFF'

  def __str__(self):
    return str(self.to_dict())
    
  def to_dict(self):
    return {'type': 'mine',
            'ID': self.ID,
            'position': self.position,
            'stock': self.stock,
            'color': self.color,
            'radius': self.radius,
            'outline': self.outline_color}

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

  def pick(self):
    self.stock += -1
