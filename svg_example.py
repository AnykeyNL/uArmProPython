# Example made by OssiLehtinen

from svgpathtools import svg2paths, wsvg
import numpy as np

import uArmRobot
import time


#Configure Serial Port
#serialport = "com3"          # for windows 
serialport = "/dev/ttyACM0"  # for linux like system

# Connect to uArm 
myRobot = uArmRobot.robot(serialport)
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

I used Inkscape to produce some test-files and everything seemed to work fine. One thing to do, is convert text to paths in Inkscape before saving.

Surely not an issue-free solution, but perhaps a starting point for something more advanced. One noticeable thing is that drawing the line segments is a bit stuttery, not sure how to improve this.

Cheers,
Ossi
 @OssiLehtinen
     
OssiLehtinen commented 10 minutes ago
The same stuff after some modifications:

Allow targeting set width of the image.
Allow lifting up the pen between paths, if such a pen is used.
from svgpathtools import svg2paths, wsvg
import numpy as np

import uArmRobot
import time

mode = 1

#Configure Serial port
#serialport = "com3"          # for windows 
serialport = "/dev/ttyACM0"  # for linux like system

# Connect to uArm 
myRobot = uArmRobot.robot(serialport)
myRobot.debug = True   # Enable / Disable debug output on screen, by default disabled
myRobot.connect()
myRobot.mode(mode)   # Set mode to Normal


steps_per_seg = 10
x_offset = 140
height = 150
draw_speed = 2500

targetWidth = 160


# Parse the path
paths, attributes = svg2paths('008.svg')


# Find the bounding box
xmin = 100000
xmax = -10000
ymin = 10000
ymax = -10000

for i in range(len(paths)):
	path = paths[i]
	attribute = attributes[i]
	# A crude check for wether a path should be drawn. Does it have a style defined? This caused trouble elsewhere...
	if 'style' in attribute:
		for seg in path:
			for p in range(steps_per_seg+1):
				cp = seg.point(float(p)/float(steps_per_seg))
				cx = np.real(cp)
				cy = np.imag(cp)
				if(cx < xmin): xmin = cx
				if(cy < ymin): ymin = cy
				if(cx > xmax): xmax = cx
				if(cy > ymax): ymax = cy


# The scaling factor to reach the targetWidth
scale = targetWidth/(xmax-xmin)
		
# Transform the paths to lists of coordinates
coords = []

for i in range(len(paths)):
	path = paths[i]
	attribute = attributes[i]
	# A crude check for wether a path should be drawn. Does it have a style defined?
	if 'style' in attribute:
		for seg in path:
			segcoords = []
			for p in range(steps_per_seg+1):
				cp = seg.point(float(p)/float(steps_per_seg))
				segcoords.append([scale*(np.real(cp)-xmin)+x_offset, scale*(np.imag(cp)-ymin) - scale*((ymax-ymin)/2.0)])
			coords.append(segcoords)



# Lift the pen if using one
move_lift = 0
if(mode == 0):
	move_lift = 5

# The starting point
myRobot.goto(coords[0][0][0], coords[0][0][1], height+move_lift*2, 6000)

lastCoord = coords[0][0]

epsilon = 0.1


	if(abs(seg[0][0] - lastCoord[0]) > epsilon and abs(seg[0][1] - lastCoord[1]) > epsilon):

for seg in coords:	
	if(abs(seg[0][0] - lastCoord[0]) > epsilon and abs(seg[0][1] - lastCoord[1]) > epsilon):
		myRobot.goto(lastCoord[0], lastCoord[1], height+move_lift, 6000)
		myRobot.goto(seg[0][0], seg[0][1], height+move_lift, 6000)
		 # Not sure if this helps with anything, but the idea is to give the arm a moment after a long transition
		time.sleep(0.15)
	for p in seg:
		myRobot.goto_laser(p[0], p[1], height, draw_speed)
	lastCoord = p


# Back to the starting point (and turn the laser off)
myRobot.goto(coords[0][0][0], coords[0][0][1], height+move_lift*2, 6000)
