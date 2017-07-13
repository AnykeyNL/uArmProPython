# Script for drawing a grid with the laser for calibration purposes

# Please, don't leave the arm unattended while operating the laser.

import uArmLaserRobot

mode = 1

#Configure Serial port
#serialport = "com3"          # for windows 
serialport = "/dev/ttyACM0"  # for linux like system

# Connect to uArm 
myRobot = uArmLaserRobot.laserRobot(serialport)
myRobot.debug = True   # Enable / Disable debug output on screen, by default disabled
myRobot.connect()
myRobot.mode(mode)   # Set mode to Normal



# Larger grid
#gridSizeX = 120
#gridSizeY = 200
#gridOffsetX = 140

# Smaller test grid
gridSizeX = 40
gridSizeY = 40
gridOffsetX = 180


workingHeight = 150
drawSpeed = 1000

# Horizontal lines 
for i in range(int(gridOffsetX/10), int((gridOffsetX+gridSizeX)/10+1)):
	print(i*10)
	myRobot.goto(i*10, -gridSizeY/2, workingHeight, 6000)
	myRobot.goto_laser(i*10, gridSizeY/2, workingHeight, drawSpeed)
	myRobot.goto(i*10, gridSizeY/2, workingHeight, 6000) # Switch the laser off

# Vertical lines
for i in range(int(-gridSizeY/20), int(gridSizeY/20+1)):
	print(i*10)
	myRobot.goto(gridOffsetX+gridSizeX, i*10, workingHeight, 6000)
	myRobot.goto_laser(gridOffsetX, i*10, workingHeight, drawSpeed)
	myRobot.goto(gridOffsetX, i*10, workingHeight, 6000) # Switch the laser off

