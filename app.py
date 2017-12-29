#!/usr/bin/python
# -*- coding:Utf-8 -*-

###################################################################################################################
# App
###################################################################################################################

import ant
import farm
import mine
import playground
import display
import Queue
import logging
import random

if __name__ == '__main__':
  FORMAT = '%(asctime)-15s: \033[95m%(type)-10s:\033[0m %(message)s'
  logging.basicConfig(format=FORMAT)
  
  SIZE = (600, 600)
  INITIAL_FARM_POS = (SIZE[0]/2 , SIZE[1]/2)
  FARM_GROWTH_RATE = 60
  FARM_SURVIVAL_TIMEOUT = 10
  FARM_MAX_ANTS = 1000
  
  disp = display.Display(SIZE, FARM_MAX_ANTS)
  display_q = disp.get_queue()
  ground = playground.Playground(SIZE)
  mine_position = (int(INITIAL_FARM_POS[0] + 100), int(INITIAL_FARM_POS[1] + 100))
  mine = mine.Mine(mine_position)
  ground.add_mine(mine)
  display_q.put(mine.to_dict())
  farm = farm.Farm(ground, display_q, INITIAL_FARM_POS, FARM_GROWTH_RATE, FARM_MAX_ANTS, FARM_SURVIVAL_TIMEOUT)
  ground.add_farm(farm)
  farm.start()
  disp.start()
