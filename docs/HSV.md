# RGB to HSV Conversion
Conversion to HSV colorspace is well suited for plant detection.
This is because plants exhibit a range of colors, generally between yellow and cyan.

# Algorithm
minima = min(r, g, b)
maxima = max(r, g, b)
value = maxima
delta = maxima - minima

if not (maxima == 0):
  saturation = delta / maxima
else:
  saturation = 0
	hue = -1

if (r == max):
  hue = (g - b) / delta # between yellow & magenta
elseif (g == max):
  hue = 2 + (b - r) / delta # between cyan & yellow
else:
  hue = 4 + (r - g) / delta #between magenta & cyan
  
hue *= 60
if (hue < 0 ):
  hue += 360
