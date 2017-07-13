import uArmLaserRobot

mode = 0

steps_per_seg = 10
x_offset = 170
height = -11
draw_speed = 100
targetWidth = 20
lineSpacing = 1.0

#Configure Serial port
#serialport = "com3"          # for windows 
serialport = "/dev/ttyACM0"  # for linux like system

# Connect to uArm 
myRobot = uArmLaserRobot.laserRobot(serialport)
myRobot.debug = True   # Enable / Disable debug output on screen, by default disabled
myRobot.connect()
myRobot.mode(mode)   # Set mode to Normal

coords = myRobot.parseSVG('bird.svg', targetWidth, x_offset, steps_per_seg)

myRobot.set_path_start(coords, height, mode)

myRobot.drawPath(coords, draw_speed, height, mode)
#myRobot.fillSVG('bird.svg', targetWidth, lineSpacing, x_offset, height, draw_speed, mode) # The bird svg doesn't have fill atm, so this is a bit silly...
myRobot.loff()

# Dock the arm before exit
myRobot.goto(225, 0, 150, 6000)
myRobot.goto(130, 0, 90, 6000)
myRobot.goto(97, 0, 30, 6000)
