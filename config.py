#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""Provides basic configuration for the Ants application.
"""

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
# CONFIG
###################################################################################################################

# -----------------------------------------------------------------------------------------------------------------
# LOGGING
# -----------------------------------------------------------------------------------------------------------------
# Logging string format
FORMAT = '%(asctime)-15s: \033[95m%(type)-10s:\033[0m %(message)s'
logging.basicConfig(format=FORMAT)

# -----------------------------------------------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------------------------------------------
WINDOW_TITLE = 'Ants: A Computer Assisted Bullshit for random life research'

# -----------------------------------------------------------------------------------------------------------------
# ANT
# -----------------------------------------------------------------------------------------------------------------
# Ant radius (Don't touch this)
ANT_RADIUS = 1
# Max number of moves for an ant
ANT_MAX_LIFE = 100000
# How many food unit an ant can carry
ANT_MAX_FOOD = 5
# How many moves an ant can remmeber
ANT_MAX_HISTORY = 300
# Ant body color when looking for food
ANT_HUNTING_COLOR = '#FF0000'
# Ant body color when looking for home
ANT_HOMING_COLOR = '#00FF00'
# Ant neutral outline color
ANT_NEUTRAL_OUTLINE_COLOR = '#FFFFFF'
# Ant outline color when lost
ANT_LOST_OUTLINE_COLOR = '#FFFF00'
# Ant outline color when busy
ANT_BUSY_OUTLINE_COLOR = '#0000FF'
# Ant outline color when dead
ANT_DEAD_OUTLINE_COLOR = '#FF0000'
# Pause delay after hailing (in seconds)
ANT_PAUSE_DELAY = 3

# -----------------------------------------------------------------------------------------------------------------
# PLAYGROUND
# -----------------------------------------------------------------------------------------------------------------
# Playground dimension
PLAYGROUND_SIZE = (600, 600)

# -----------------------------------------------------------------------------------------------------------------
# FARM
# -----------------------------------------------------------------------------------------------------------------
# Farm poistion
FARM_POS = (PLAYGROUND_SIZE[0]/2 , PLAYGROUND_SIZE[0]/2)
# How many ants by minute a farm can pop an ant
# MUST be <= 60
FARM_GROWTH_RATE = 60
# How many time in minutes a farm can survive without food stock
FARM_SURVIVAL_TIMEOUT = 10
# Radius of a farm
FARM_RADIUS = 20
# Food stock of newly created farm 
FARM_INITIAL_FOOD_STOCK= 100
# Farm body color
FARM_COLOR = '#4B1BB4'
# Farm outline color
FARM_OUTLINE_COLOR = '#FFFFFF'

# -----------------------------------------------------------------------------------------------------------------
# Mine
# -----------------------------------------------------------------------------------------------------------------
# Radius of a mine
MINE_RADIUS = 20
# Mine body color
MINE_COLOR = '#EF26AD'
# Mine outline color
MINE_OUTLINE_COLOR = '#FFFFFF'
# Mine initial amount of food
MINE_INITIAL_STOCK = 1000
