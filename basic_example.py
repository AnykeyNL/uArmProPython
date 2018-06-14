# uArm Swift Pro - Python Library Example
# Created by: Richard Garsthagen - the.anykey@gmail.com
# V0.3 - June 2018 - Still under development
#
# Use Python 2.x!

import uArmRobot
import time

#Configure Serial Port
serialport = "com10"          # for windows 
#serialport = "/dev/ttyACM0"  # for linux like system

# Connect to uArm 
myRobot = uArmRobot.robot(serialport,1)   # user 0 for firmware < v4 and use 1 for firmware v4
myRobot.debug = True  # Enable / Disable debug output on screen, by default disabled
myRobot.connect()
myRobot.mode(0)   # Set mode to Normal

time.sleep(1)

# Move robot, command will complete when motion is completed
myRobot.goto(200,0,100,6000)

# Turn on the pump
myRobot.pump(True)

# Send move command, but continue program
myRobot.async_goto(200,150,250,3000)
while myRobot.moving:
    print ("Waiting to complete move")
    time.sleep(0.5)

#Turn off the pump
myRobot.pump(False)

# Send move command, but continue program
myRobot.async_goto(200,0,100,6000)
while myRobot.moving:
    print ("Waiting to complete move")
    time.sleep(0.5)


time.sleep(5)

#Disconnect serial connection
myRobot.disconnect()
