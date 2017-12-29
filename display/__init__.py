#!/usr/bin/python
# -*- coding:Utf-8 -*-

###################################################################################################################
# Display
###################################################################################################################

from Tkinter import *
import Queue
import threading
import logging
import time

class Worker(threading.Thread):
  def __init__(self, display, ID, queue):
    threading.Thread.__init__(self)
    self.ID = ID
    self.display = display
    self.queue = queue
    self.active = True

  def run(self):
    data = {'type': 'Display worker %d' % self.ID}
    logging.warning('\033[92mStatus:\033[0m %s' % self.active, extra=data)
    while self.active:
      item = self.queue.get()
      self.process(item)
    logging.warning('\033[92mStatus:\033[0m %s' % self.active, extra=data)

  def process(self, item):
    data = {'type': 'Display worker %d: [%s]' % (self.ID, item['type'])}
    logging.warning('\033[92mData:\033[0m %s' % (str(item)), extra=data)
    if item['type'] == 'ant':
      self.display.draw_ant(item['ID'], item['old_position'], item['new_position'], item['color'])
    elif item['type'] == 'farm':
      pass
    elif item['type'] == 'mine':
      self.display.draw_mine(item['ID'], item['position'], item['color'])

  def stop(self):
    self.active = False

class Display(object):
  def __init__(self, size, max_ants):
    self.display_q = Queue.Queue()
    self.width, self.height = size
    self.master = Tk()
    self.workers = {}
    for w in xrange(max_ants):
      self.workers[w] = Worker(self, w, self.display_q)
      self.workers[w].start()
    self.build_gui()
    self.update_gui()

  def get_queue(self):
    return self.display_q

  def build_gui(self):
    self.canvas_frame = LabelFrame(self.master, width=self.width+10, height=self.height+10, text='Ants')
    self.canvas = Canvas(self.canvas_frame, width=self.width, height=self.height, background='black', relief=SUNKEN)
    self.canvas.grid()
    self.canvas_frame.grid(row=0, column=0)

  def draw_ant(self, ID, old_pos, new_pos, color):
    if len(self.canvas.find_withtag(ID)) > 0:
      x_offset = old_pos[0] - new_pos[0]
      y_offset = old_pos[1] - new_pos[1]
      self.canvas.move(ID, x_offset, y_offset)
    else:
      self.canvas.create_line(new_pos[0], new_pos[1], new_pos[0], new_pos[1], tags=ID, width=8, capstyle=ROUND, joinstyle=ROUND, fill=color)
    self.update_gui()

  def draw_mine(self, ID, pos, color):
    self.canvas.create_line(pos[0], pos[1], pos[0], pos[1], tags=ID, width=20, capstyle=ROUND, joinstyle=ROUND, fill=color)
    self.update_gui()

  def update_gui(self):
    self.canvas.update()

  def start(self):
    self.master.mainloop()
