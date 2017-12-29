#!/usr/bin/python
# -*- coding:Utf-8 -*-

###################################################################################################################
# Utils
###################################################################################################################

import random

directions = { 0: [0, 0],
               1: [1, 0],
               2: [-1, 0],
               3: [0, -1],
               4: [0, 1],
               5: [-1, 1],
               6: [1, 1],
               7: [1, -1],
               8: [-1, -1]
             }

def gen_color():
  alpha = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')
  return '#%s' % ''.join([random.choice(alpha) for _ in range(6)])