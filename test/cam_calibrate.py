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

p = 1
while (p <= totalP):
    detect =0
    raw_input ("Place coin [{}] in a corner".format(p))
    while detect ==0:
        cx,cy,cr = easycv2.getCircle(25)
        if cr ==0:
            raw_input("no coin detected, try again")
        else:
            detect = 1
            coins.append([cx,cy,cr])
    
    raw_input ("Place uArm on coin")
    myRobot.get_coor()
    points.append([myRobot.X, myRobot.Y, myRobot.Z])
    print ("X: {}  Y:{}  Z:{}".format(myRobot.X, myRobot.Y, myRobot.Z))
    p = p + 1

p = 0
while (p < totalP):
    print ("uARM: {},{}\tCam: {},{}".format(points[p][0],points[p][1],coins[p][0],coins[p][1]))
    p = p + 1

myRobot.motors_on(True)
myRobot.goto(120, 0, 30,20)
     
#Disconnect serial connection
myRobot.disconnect()
