# uArm Swift Pro - Python Library Example
# Created by: Richard Garsthagen - the.anykey@gmail.com
# V0.3 - June 2018 - Still under development
#
# Use Python 2.x!

import uArmRobot
import time
import easycv2

points = []
coins = []
totalP = 4
speed = 80

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
myRobot.goto(120, 0, 30,20)
time.sleep(1)
print ("Releasing motors")
myRobot.motors_on(False)

raw_input("press enter")


myRobot.get_coor()
x,y,z = [myRobot.X, myRobot.Y, myRobot.Z]

print ("X: {}  Y:{}  Z:{}".format(x,y,z))

myRobot.motors_on(True)
myRobot.goto(120, 0, 30,20)
time.sleep(1)
myRobot.goto(x,y,30,20)
myRobot.goto(x,y,z,20)

     
#Disconnect serial connection
myRobot.disconnect()
