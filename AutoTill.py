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
import datetime

# Declarations
NUM_CAMERAS = 2
RUN_MODE = 'verbose'
LOGNAME = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.csv'
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
    def __init__(self, num_cameras=1, run_mode='quiet'):
        print('[Initializing]')
        self.run_mode = run_mode
        self.num_cameras = num_cameras
        self.history = SAMPLES*[CENTER]
        self.cameras = []
        for index in range(num_cameras):
            cam = cv2.VideoCapture(index)
            cam.set(3, WIDTH)
            cam.set(4, HEIGHT)
            self.cameras.append(cam)

    ## Identify Plants
    def find_plants(self):
        print('[Finding Crop Row]')
        offsets = []
        for cam in self.cameras:
            (s,rgb) = cam.read()
            if not rgb == None:
                hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
                sat_min = hsv[:,:,1].mean()
                val_min = hsv[:,:,2].mean()
                hue_min = numpy.array([40, sat_min, val_min], numpy.uint8)
                hue_max = numpy.array([80, 255, 255], numpy.uint8)
                egi = cv2.inRange(hsv, hue_min, hue_max)
                offset = egi.sum(axis=0).argmax() - CENTER
                offsets.append(offset)
            else:
                return None
        return offsets

    ## Adjust cultivator mechanics
    def adjust_cultivator(self, offsets):
        print('[Adjusting Cultivator Steering]')
        if not offsets == None:
            average = numpy.mean(offsets)
            adjusted = average
            left_cycle = HALF_DUTY + (HALF_DUTY * adjusted)/CENTER
            right_cycle = HALF_DUTY - (HALF_DUTY * adjusted)/CENTER
            # left.ChangeDutyCycle(left_cycle)
            # right.ChangeDutyCycle(right_cycle)
            return (left_cycle, right_cycle)
        else:
            return None

    ## Stop program safely 
    def close(self):
        print('[Releasing Cameras]')
        for cam in self.cameras:
            cam.release()
  
    ## Run
    def run(self):
        print('[Running Guidance System]')
        try:
            while True:
                offsets = self.find_plants()
                cycles = self.adjust_cultivator(offsets)
        except KeyboardInterrupt:
            self.close()
    
# Main
if __name__ == "__main__":
  root = AutoTill(num_cameras=NUM_CAMERAS, run_mode=RUN_MODE)
  root.run()
