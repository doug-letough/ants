#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""The ants module entry point.
"""

import config
import ant
import farm
import mine
import playground
import display
import logging
import random
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
# App
###################################################################################################################

if __name__ == '__main__':
  # The display
  disp = display.Display(config.PLAYGROUND_SIZE, config.FARM_INITIAL_FOOD_STOCK)
  # The FIFO queue to communicate with display
  display_q = disp.get_display_queue()
  # The queue needed to have response back from display to playground
  response_q = disp.get_response_queue()
  # Create play ground
  ground = playground.Playground(config.PLAYGROUND_SIZE, response_q)
  # Create a food mine
  mine_position = (int(config.FARM_POS[0] + 110), int(config.FARM_POS[1] + 110))
  mine = mine.Mine(mine_position, config.MINE_RADIUS)
  # Add the mine to the playground
  ground.add_mine(mine)
  # Display the mine
  display_q.put(mine.to_dict())
  # Create the farm
  farm = farm.Farm(ground,
                   display_q,
                   config.FARM_POS,
                   config.FARM_GROWTH_RATE,
                   config.FARM_INITIAL_FOOD_STOCK,
                   config.FARM_SURVIVAL_TIMEOUT,
                   config.FARM_RADIUS)
  # Add farm to the playground
  ground.add_farm(farm)
  # Display farm
  display_q.put(farm.to_dict())
  # Start the farm own process
  farm.start()
  # Start the display own process
  disp.start()
