import easycv2
import uArmRobot
import time


r = easycv2.Calibrate(25)

serialport = "com10"
myRobot = uArmRobot.robot(serialport,1)   # user 0 for firmware < v4 and use 1 for firmware v4
myRobot.debug = True  # Enable / Disable debug output on screen, by default disabled
myRobot.connect()
myRobot.mode(0)   # Set mode to Normal
time.sleep(1)

myRobot.goto(300,-100,10,20)

time.sleep(2)

myRobot.disconnect()
