#!/usr/bin/python
"""
Name: AutoTill
Author: Trevor Stanhope
Organization: Bioresource Engineering, McGill University
Summary: USB camera computer vision cultivator guidance system.
Requires: Python 2.x, OpenCV 2.4.7, Numpy
"""

# Imports
import numpy # image processing
import cv2
import time
import sys

# Declarations
LOGNAME = 'test.csv'
RATE = 4096 # 5 volt per 4096 Hz
LEFT_PIN = 24
RIGHT_PIN = 25
WIDTH = 320
HEIGHT = 240
CENTER = WIDTH/2.0
HALF_DUTY = 50.0
SAMPLES = 5

# AutoTill
class AutoTill:

  ## Initialize
  def __init__(self, cameras):
    self.left_cycle = HALF_DUTY
    self.right_cycle = HALF_DUTY
    self.current = CENTER
    self.history = SAMPLES*[CENTER]

    self.cameras = []
    for index in range(cameras):
      cam = cv2.VideoCapture(index)
      cam.set(3, WIDTH)
      cam.set(4, HEIGHT)
      self.cameras.append(cam)

  ## Identify Plants
  def find_plants(self):
    self.images = []
    self.offsets = []
    a = time.time()
    for cam in self.cameras:
      (s,rgb) = cam.read()
      hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
      sat_min = hsv[:,:,1].mean()
      val_min = hsv[:,:,2].mean()
      GREEN_MIN = numpy.array([30, sat_min, val_min], numpy.uint8)
      GREEN_MAX = numpy.array([70, 255, 255], numpy.uint8)
      egi = cv2.inRange(hsv, GREEN_MIN, GREEN_MAX)
      columns = egi.sum(axis=0)
      offset = columns.argmax() - CENTER
      self.offsets.append(offset)
      self.images.append(egi)
    b = time.time()
    self.frequency = int(1/(b-a))

  ## Adjust cultivator mechanics
  def adjust_cultivator(self):
    self.history.pop(0)
    self.current = numpy.mean(self.offsets)
    self.history.append(self.current)
    self.adjusted = numpy.mean(self.history)
    self.left_cycle = HALF_DUTY + (HALF_DUTY*self.adjusted)/CENTER
    self.right_cycle = HALF_DUTY - (HALF_DUTY*self.adjusted)/CENTER
    # left.ChangeDutyCycle(self.left_cycle)
    # right.ChangeDutyCycle(self.right_cycle)
  
  ## Display current values
  def display(self, mode):
    print('Frequency: %s Hz' % self.frequency)
    print('Current Offset: %s px' % self.current)
    print('Difference: %s px' % self.adjusted)
    print('Left Cycle: %s %%' % self.left_cycle)
    print('Right Cycle: %s %%' % self.right_cycle)
    print('History: %s' % self.history)
    print('----------------------------------')
    with open(LOGNAME, 'a') as log:
      log.write(str(self.current) + ',' + str(self.left_cycle) + '\n')
    
    if mode:
      for image in self.images:
        image[:,self.current + CENTER] = 128
        image[:,self.adjusted + CENTER] = 254  
        cv2.imshow("EGI", image)
        cv2.waitKey(0)

  ## Stop program safely 
  def close(self):
    for cam in self.cameras:
      print('Releasing Camera')
      cam.release()

if __name__ =='__main__':
  
  try:
    mode = sys.argv[1]
  except Exception:
    mode = False
  try:
    cameras = int(sys.argv[2])
  except Exception:
    cameras = 1

  root = AutoTill(cameras)
  try:
    while True:
      root.find_plants()
      root.adjust_cultivator()
      root.display(mode)
  except KeyboardInterrupt:
    root.close()
