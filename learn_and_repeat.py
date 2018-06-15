# uArm Swift Pro - Python Library Example
# Created by: Richard Garsthagen - the.anykey@gmail.com
# V0.3 - June 2018 - Still under development
#
# Use Python 2.x!

import uArmRobot
import time

points = []
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
myRobot.goto(200,0,20,60)
print ("Releasing motors")
myRobot.motors_on(False)

p = 1
while (p <= totalP):
    raw_input ("Place uArm on point {}".format(p))
    myRobot.get_coor()
    points.append([myRobot.X, myRobot.Y, myRobot.Z])
    print ("X: {}  Y:{}  Z:{}".format(myRobot.X, myRobot.Y, myRobot.Z))
    p = p + 1

# Disconnecting and reconnecting. If you just turn motors back on, the movement does not seem to work

raw_input ("Place uArm in middle and press enter to start repeat sequence")
myRobot.disconnect()
time.sleep(1)
myRobot.connect()
time.sleep(1)
myRobot.goto(200,0,200,speed)
time.sleep(1)

while True:
    for p in points:
        print ("X: {}  Y:{}  Z:{}".format(p[0], p[1], 10))
        myRobot.goto(p[0],p[1],p[2]+20,speed)
        myRobot.goto(p[0],p[1],p[2],speed)
        myRobot.goto(p[0],p[1],p[2]+20,speed)
        
#Disconnect serial connection
myRobot.disconnect()
