#!/usr/bin/python
# -*- coding:Utf-8 -*-

###################################################################################################################
# Mine
###################################################################################################################

import uuid
import utils
import random

class Mine(object):
  def __init__(self, position):
    self.position = position
    self.ID = str(uuid.uuid4())
    self.stock = 1000
    self.color = utils.gen_color()
    
  def __str__(self):
    return str(self.to_dic())
    
  def to_dict(self):
    return {'type': 'mine', 'ID': self.ID, 'position': self.position, 'stock': self.stock, 'color': self.color}

  def pick(self):
    self.stock += -1
