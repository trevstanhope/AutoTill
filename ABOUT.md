# AutoTill
## Overview
AutoTill is an automated path following system using computer vision to control a cultivator. AutoTill is specifically focused on organic farming, and allows earlier tilling of cropland for immature row crops.
    
## Controller System
The AutoTill controller uses a RaspberryPi Revision B microcomputer running Debian Linux. Additionally, the system is interfaced with a USB camera and wireless card. To simplify troubleshooting, the onboard wireless card allows any wirelessly enabled computer to communicate with the device while it is powered on. All that is necessary is to create an open Ad-hoc wireless network with the ESSID "AutoTill", restart the device, and it will automatically connect to the network. Then by use of SSH the user account "pi" device can be manually accessed with the password "password".
    
## Camera
The USB camera can be fixed to any solid element in line with the crop path, and should be adjusted to within 8" from the soil surface. The camera has a 90 degree field of view and at a height of 8" the resulting image is 8" in width. This height is ideal for cultivator systems as most require 4" maximum in either direction, however the height can be adjusted as necessary for different applications. To prevent dust build-up on the lens, a PVC lens jacket has been fit around the camera. A 1/4" air hose supplied by the tractor's compressor provides a constant stream of air into the lens jacket, agitating dust away from the lens.
    
## Application
On boot, a python application named AutoTill.py is executed. This script relies on the OpenCV and NumPy libraries to process the video stream for plant-like objects. The x-offset of these objects is then used to drive two PWM I/O pins on the board which are connected to the cultivator's guidance system. The two PWM outputs supply complimentary voltages totaling 5V, where the difference represents the degree from center that the cultivator needs to be adjusted. 

## Plant Finding Algorithm
To allow for the fastest possible processing speed of the video stream, the algorithm used is very simple and only considers the x-offset of objects in the image, not the y-offset. As each RGB image is captured, the algorithm parses only the green channel (G) as a 2-dimensional numeric array of pixel intensities. Each column of pixels is then summated, given a 1-dimensional array of length equal to the pixel width of the image captured. For optimization purposes, the image width is set to 160px, as higher resolutions are not necessary for the low height of the camera. Lastly, the algorithm  returns the index for the maximum value of this 1-dimensional array, which represents the degree from the left-hand side of the image where the greenest objects are located.
    
To compensate for aberrations in the algorithm, the results of the last several images are stored and the output PWM is calculated from the mean of these values, instead of the most recent value. This also serves to compensate for long patches of no plants.
    
## Data Logging
In the event that you wish to review the results of a run, the position of the offsets are logged continously.

## Future Improvements
The following is a list of possible improvements to the AutoTill system:
1. Accelerometer vibration compensation
2. Database logging
3. WAN connection
4. Automatically populated system updates
