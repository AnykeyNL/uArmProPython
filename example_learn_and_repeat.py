# uArm Swift Pro - Python Library Example
# Created by: Richard Garsthagen - the.anykey@gmail.com
# V0.3 - June 2018 - Still under development
#
# Use Python 2.x!
#
# Basic learn / readout location and return to that location.

import uArmRobot
import time

speed = 80
flying_height= 50

#Configure Serial Port
serialport = "com10"          # for windows 
#serialport = "/dev/ttyACM0"  # for linux like system

# Connect to uArm 
myRobot = uArmRobot.robot(serialport,1)   # user 0 for firmware < v4 and use 1 for firmware v4
myRobot.debug = True  # Enable / Disable debug output on screen, by default disabled
myRobot.connect()
myRobot.mode(0)   # Set mode to Normal
time.sleep(1)

# Goto Home position
myRobot.goto(120, 0, flying_height ,speed)
time.sleep(1)
myRobot.motors_on(False)
print ("Releasing motors, place the robot on any spot")
raw_input("== press enter ==")

# Read out location of the uArm
myRobot.get_coor()
x,y,z = [myRobot.X, myRobot.Y, myRobot.Z]
print ("Robot is at X: {}  Y:{}  Z:{}".format(x,y,z))

# Move up, Return home and go back to learned position
myRobot.motors_on(True)
myRobot.goto(x, y, flying_height,speed)
myRobot.goto(120, 0, flying_height,speed)
time.sleep(1)
myRobot.goto(x,y,flying_height,speed)
myRobot.goto(x,y,z,speed)
     
#Disconnect serial connection
myRobot.disconnect()
