#!/usr/bin/env python
# -*- coding:Utf-8 -*-

"""Provides Worker and Display classes.

NumberList holds a sequence of numbers, and defines several statistical
operations (mean, stdev, etc.) FrequencyDistribution holds a mapping from
items (not necessarily numbers) to counts, and defines operations such as
Shannon entropy and frequency normalization.
"""

from Tkinter import *
import Queue
import threading
import logging
import time
import atexit

__author__ = "Doug Le Tough"
__copyright__ = "Copyright 2017, Doug Le Tough"
__credits__ = ["Doug Le Tough",]
__license__ = "WTFPL"
__version__ = "1.0.0"
__maintainer__ = "Doug Le Tough"
__email__ = "doug.letough@free.fr"
__status__ = "Testing"

###################################################################################################################
# Display
###################################################################################################################



class Worker(threading.Thread):
  """ The Worker object provides a way to process data found in a queue.
      When data is found, it is parsed and then displayed accordingly.

      The Worker object runs in its own thread.
  """
  def __init__(self, display, ID, queue):
    """
    display: The display on wich data are displayed
    ID: The Worker instance ID
    queue: The FIFO queue where the data have to be collected
    """
    threading.Thread.__init__(self)
    self.ID = ID
    self.display = display
    self.queue = queue
    self.active = True
    self.data = {'type': 'Display worker %d' % self.ID}

  def run(self):
    """
    The Worker thread main loop:
    - Get data from queue and give it to the process method
    """
    logging.warning('\033[93mReport status:\033[0m \033[92mActive:\033[0m %s' % self.active, extra=self.data)
    while self.active:
      try:
        item = self.queue.get(False)
        self.process(item)
      except Queue.Empty:
        pass
    logging.warning('\033[93mReport status:\033[0m \033[92mActive:\033[0m %s' % self.active, extra=self.data)

  def process(self, item):
    """
    Displays received item.
    Item must be a dict (JSON like hash)
    Valid data can be one of the 3 following type:
    - ant
    - farm
    - mine
    """
    if item['type'] == 'ant':
      self.display.draw_ant(item['ID'], item['old_position'], item['new_position'], item['radius'], item['color'], item['outline'])
    elif item['type'] == 'farm':
      self.display.draw_farm(item['ID'], item['position'], item['radius'], item['color'], item['outline'])
    elif item['type'] == 'mine':
      self.display.draw_mine(item['ID'], item['position'], item['radius'], item['color'], item['outline'])

  def stop(self):
    """
    Exit from main loop
    """
    self.active = False

class Display(object):
  """
  The Display object is the main interface to TKInter display.
  Basically it is a simple Canvas with a frame inside a window.

  Data processed by workers are displayed inside the canvas.
  """
  def __init__(self, size, max_ants):
    """
    size: The display size. Should be equal to config.PLAYGROUND_SIZE
    max_ants: The estimated maximum number of ants

    Since the number of living ants can not be guessed or guaranted, the max_ants
    is an estimation.
    It's a good idea to make it equal to config.FARM_INITIAL_FOOD_STOCK.

    The max_ants value will determine the number of workers created by the Display object.
    """
    # The display queue. Workers will write to it.
    self.data = {'type': 'Display'}
    self.display_q = Queue.Queue()
    self.response_q = Queue.Queue()
    self.width, self.height = size
    # The main Tk window
    self.master = Tk()
    self.workers = {}
    # Register the stop() method with atexit module
    self.master.protocol("WM_DELETE_WINDOW", self.stop)
    # Create all needed workers
    for w in xrange(max_ants):
      self.workers[w] = Worker(self, w, self.display_q)
      self.workers[w].start()
    # Build the GUI
    self.build_gui()
    # Update the display
    self.update_gui()

  def get_display_queue(self):
    """ Returns the display queue"""
    return self.display_q

  def get_response_queue(self):
    """ Returns the response queue"""
    return self.response_q

  def build_gui(self):
    """ Build the GUI with widgets from Tkinter module """
    self.canvas_frame = LabelFrame(self.master, width=self.width+10, height=self.height+10, text='Ants')
    self.canvas = Canvas(self.canvas_frame, width=self.width, height=self.height, background='black', relief=SUNKEN)
    self.canvas.grid()
    self.canvas_frame.grid(row=0, column=0)

  def draw_ant(self, ID, old_pos, new_pos, radius, color, outline):
    """
    Draw an non existent ant according to data received.
    If ant already exists, the ant is moved to new_pos coordinates.
    
    ID: The ant ID
    old_pos: The previous position of this ant
    new_pos: The new position where this ant must be displayed
    radius: The ant radius (Don't touch this: see config.ANT_RADIUS)
    color: The ant body color
    outline: The ant outline color
    """
    if len(self.canvas.find_withtag(ID)) > 0:
      # Ant already exists so we compute the new_pos/old_pos offset 
      x_offset = new_pos[0] - old_pos[0]
      y_offset = new_pos[1] - old_pos[1]
      self.canvas.itemconfig(ID, fill=color, outline=outline)
      self.canvas.move(ID, x_offset, y_offset)
    else:
      # Ant is new
      self.canvas.create_oval(new_pos[0] - radius, new_pos[1] - radius , new_pos[0] + radius , new_pos[1] + radius, tags=ID, fill=color, outline=outline)
      # Put the ant up in the higher layer
      self.canvas.tag_raise(ID)
    self.update_gui()

  def draw_mine(self, ID, pos, radius, color, outline):
    """
    Draw an non existent mine according to data received.
    
    ID: The mine ID
    pos: The position of this mine
    radius: The mine radius (see config.MINE_RADIUS)
    color: The mine body color (see config.MINE_COLOR)
    outline: The mine outline color (see config.MINE_OUTLINE_COLOR)
    """
    ux = pos[0] - radius
    uy = pos[1] - radius
    dx = pos[0] + radius
    dy = pos[1] + radius
    logging.warning('\033[93mDraw mine:\033[0m %s, \033[92mux:\033[0m %d, \033[92muy:\033[0m %d, \033[92mdx:\033[0m %d, \033[92mdy:\033[0m %d' % (ID, ux, uy, dx, dy), extra=self.data)
    self.canvas.create_oval(ux, uy, dx, dy, tags=ID, fill=color, outline=outline)
    # Put the mine down in the lower layer
    self.canvas.tag_lower(ID)
    self.update_gui()

  def draw_farm(self, ID, pos, radius, color, outline):
    """
    Draw an non existent farm according to data received.
    
    ID: The farm ID
    pos: The position of this farm
    radius: The farm radius (see config.FARM_RADIUS)
    color: The farm body color (see config.FARM_COLOR)
    outline: The mine outline color (see config.FARM_OUTLINE_COLOR)
    """
    ux = pos[0] - radius
    uy = pos[1] - radius
    dx = pos[0] + radius
    dy = pos[1] + radius
    logging.warning('\033[93mDraw farm:\033[0m %s, \033[92mux:\033[0m %d, \033[92muy:\033[0m %d, \033[92mdx:\033[0m %d, \033[92mdy:\033[0m %d' % (ID, ux, uy, dx, dy), extra=self.data)
    self.canvas.create_oval(ux, uy, dx, dy, tags=ID, fill=color, outline=outline)
    # Put the farm down in the lower layer
    self.canvas.tag_lower(ID)
    self.update_gui()

  def update_gui(self):
    """ Update the canvas """
    self.canvas.update()

  def start(self):
    """ Start the window main loop of events """
    self.master.mainloop()

  def stop(self):
    """ Send stop signal to all objects (ants, farms, mines, workers)"""
    logging.warning('\033[93mSending kill signal\033[0m', extra=self.data)
    self.response_q.put({'type': 'kill'})
    for worker in self.workers:
      self.workers[worker].stop()
    self.master.destroy()
    logging.warning('\033[93mExiting\033[0m', extra=self.data)
    exit(0)
