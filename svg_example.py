# Example made by OssiLehtinen
#

from svgpathtools import svg2paths, wsvg
import numpy as np

import uArmRobot
import time


#Configure Serial Port
#serialport = "com3"          # for windows 
serialport = "/dev/ttyACM0"  # for linux like system

# Connect to uArm 
myRobot = uArmRobot.robot(serialport,0) # user 0 for firmware < v4 and use 1 for firmware v4
myRobot.debug = True   # Enable / Disable debug output on screen, by default disabled
myRobot.connect()
myRobot.mode(1)   # Set mode to Normal

# Read in the svg
paths, attributes = svg2paths('drawing.svg')

scale = .25
steps_per_seg = 3
coords = []
x_offset = 200
height = 90
draw_speed = 1000

# Convert the paths to a list of coordinates
for i in range(len(paths)):
	path = paths[i]
	attribute = attributes[i]
	# A crude check for whether a path should be drawn. Does it have a style defined?
	if 'style' in attribute:
		for seg in path:
			segcoords = []
			for p in range(steps_per_seg+1):
				cp = seg.point(float(p)/float(steps_per_seg))
				segcoords.append([-np.real(cp)*scale+x_offset, np.imag(cp)*scale])
			coords.append(segcoords)




# The starting point
myRobot.goto(coords[0][0][0], coords[0][0][1], height, 6000)


for seg in coords:	
	myRobot.goto(seg[0][0], seg[0][1], height, 6000)
	time.sleep(0.15)
	for p in seg:
		myRobot.goto_laser(p[0], p[1], height, draw_speed)
	


# Back to the starting point (and turn the laser off)
myRobot.goto(coords[0][0][0], coords[0][0][1], height, 6000)
