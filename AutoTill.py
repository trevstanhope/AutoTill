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

# Declarations
LOGNAME = 'test.csv'
RATE = 4096 # 5 volt per 4096 Hz
LEFT_PIN = 24
RIGHT_PIN = 25
CAMERA_INDEX = 0
WIDTH = 640
HEIGHT = 480
CENTER = WIDTH/2.0
MINIMA = 1.0
HALF_DUTY = 50.0
GREEN_MIN = numpy.array([20, 50, 50],numpy.uint8)
GREEN_MAX = numpy.array([60, 255, 255],numpy.uint8)
SAMPLES = 5

# AutoTill
class AutoTill:

  ## Initialize
  def __init__(self):
    self.time = 0
    self.difference = 0
    self.left_cycle = HALF_DUTY
    self.right_cycle = HALF_DUTY
    self.current = CENTER
    self.previous = CENTER
    self.camera = cv2.VideoCapture(CAMERA_INDEX)
    self.camera.set(3, WIDTH)
    self.camera.set(4, HEIGHT)
    self.history = SAMPLES*[0]
    self.image = None
  
  ## Identify Plants
  def find_plants(self):
    a = time.time()
    (s,rgb) = self.camera.read()
    hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
    sat_min = hsv[:,:,1].mean()
    val_min = hsv[:,:,2].mean()
    GREEN_MIN = numpy.array([30, sat_min, val_min], numpy.uint8)
    GREEN_MAX = numpy.array([70, 255, 255], numpy.uint8)
    egi = cv2.inRange(hsv, GREEN_MIN, GREEN_MAX)
    columns = egi.sum(axis=0)
    b = time.time()
    self.previous = self.current
    self.current = columns.argmax() - CENTER
    self.difference = self.current - self.previous
    self.frequency = int(1/(b-a))
    self.image = egi

  ## Adjust cultivator mechanics
  def adjust_cultivator(self):
    self.history.pop(0)
    self.history.append(self.current)
    self.adjusted = numpy.mean(self.history)
    self.left_cycle = HALF_DUTY + (HALF_DUTY*self.adjusted)/CENTER
    self.right_cycle = HALF_DUTY - (HALF_DUTY*self.adjusted)/CENTER
    # left.ChangeDutyCycle(self.left_cycle)
    # right.ChangeDutyCycle(self.right_cycle)
  
  ## Display current values
  def display(self):
    print('Frequency: %s Hz' % self.frequency)
    print('Previous Offset: %s px' % self.previous)
    print('Current Offset: %s px' % self.current)
    print('Difference: %s px' % self.difference)
    print('Left Cycle: %s %%' % self.left_cycle)
    print('Right Cycle: %s %%' % self.right_cycle)
    print('History: %s' % self.history)
   
    with open(LOGNAME, 'a') as log:
      log.write(str(self.current) + ',' + str(self.left_cycle) + '\n')
    self.image[:,self.current + CENTER] = 128
    self.image[:,self.adjusted + CENTER] = 254  
    cv2.imshow("EGI", self.image)
    cv2.waitKey(0)
    print('----------------------------------')

  ## Stop program safely 
  def close(self):
    print('Releasing Camera')
    self.camera.release()

if __name__ =='__main__':
  session = AutoTill()
  try:
    while True:
      session.find_plants()
      session.adjust_cultivator()
      session.display()
  except KeyboardInterrupt:
    session.close()
