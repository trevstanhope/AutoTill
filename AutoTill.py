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
import sys, getopt

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
  def __init__(self, mode=0, cameras=1):
    self.left_cycle = HALF_DUTY
    self.right_cycle = HALF_DUTY
    self.current = CENTER
    self.history = SAMPLES*[CENTER]
    self.mode = mode
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
      GREEN_MIN = numpy.array([40, sat_min, val_min], numpy.uint8)
      GREEN_MAX = numpy.array([80, 255, 255], numpy.uint8)
      RED_MIN = numpy.array([0, 0, val_min], numpy.uint8)
      RED_MAX = numpy.array([0, 255, 255], numpy.uint8)
      BLUE_MIN = numpy.array([60, sat_min, val_min], numpy.uint8)
      BLUE_MAX = numpy.array([120, 255, 255], numpy.uint8)
      if (sat_min > 60):
        print('DAYLIGHT MODE')
        egi = cv2.inRange(hsv, GREEN_MIN, GREEN_MAX)
        g_columns = egi.sum(axis=0)
        offset = g_columns.argmax() - CENTER
      elif (sat_min > 30):
        print('LOWLIGHT MODE')
        ebi = cv2.inRange(hsv, BLUE_MIN, BLUE_MAX)
        b_columns = ebi.sum(axis=0)
        offset = b_columns.argmax() - CENTER 
      else:
        print('NIGHT MODE')
        eri = cv2.inRange(hsv, RED_MIN, RED_MAX)
        r_columns = eri.sum(axis=0)
        offset = r_columns.argmax() - CENTER
      self.offsets.append(offset)
      self.images.append(rgb) # image to save
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
  def display(self):
    print('Frequency: %s Hz' % self.frequency)
    print('Current Offset: %s px' % self.current)
    print('Difference: %s px' % self.adjusted)
    print('Left Cycle: %s %%' % self.left_cycle)
    print('Right Cycle: %s %%' % self.right_cycle)
    print('History: %s' % self.history)
    print('----------------------------------')
    with open(LOGNAME, 'a') as log:
      log.write(str(self.current) + ',' + str(self.left_cycle) + '\n')
    
    if self.mode == 1:
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

def main(argv):
  mode = 0
  cameras = 1
  try:
    opts, args = getopt.getopt(argv, "d:c:")
  except getopt.GetoptError:
    print 'usage: AutoTill.py [options]'
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h'):
      print '-d for developer mode, -c <num> for number cameras'
      sys.exit(2)
    elif opt in ("-d"):
      print 'Developer mode selected'
      mode = 1
    elif opt in ("-c"):
      cameras = int(arg)    
  return mode, cameras

if __name__ == "__main__":
  (mode, cameras) = main(sys.argv[1:])
  root = AutoTill(cameras=cameras, mode=mode)
  try:
    while True:
      root.find_plants()
      root.adjust_cultivator()
      root.display()
  except KeyboardInterrupt:
    root.close()
