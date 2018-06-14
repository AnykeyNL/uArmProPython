# uArm Swift Pro - Python Library Example
# Created by: Richard Garsthagen - the.anykey@gmail.com
# V0.3 - June 2018 - Still under development
#
# Use Python 2.x!

import uArmRobot
import time

bots = 2

#Configure Serial Port
myRobot = []
myRobot.append(uArmRobot.robot("com3",0)) # user 0 for firmware < v4 and use 1 for firmware v4
myRobot.append(uArmRobot.robot("com4",0)) # user 0 for firmware < v4 and use 1 for firmware v4



#  Enable / Disable debug output on screen, by default disabled
#uArmRobot.robot.debug = True

# Connect to all the robots
for b in range(0,bots):
    myRobot[b].connect()
    myRobot[b].mode(0)  

time.sleep(1)

# Move robot one by one
print ("Move 1")
for b in range(0,bots):
    myRobot[b].goto(200,0,100,6000)


# Move all robots at same time
print ("Move 2")
for b in range(0,bots):
    myRobot[b].async_goto(200,-150,250,6000)

moving = True
while moving:
    moving = False
    for b in range(0,bots):
        if myRobot[b].moving: moving=True
        time.sleep(0.1)


print ("Move 3")
for b in range(0,bots):
    myRobot[b].async_goto(200,150,50,6000)

moving = True
while moving:
    moving = False
    for b in range(0,bots):
        if myRobot[b].moving: moving=True
        time.sleep(0.1)

print ("all done")

time.sleep(5)

#Disconnect serial connection
for b in range(0,bots):
    myRobot[b].disconnect()

    




