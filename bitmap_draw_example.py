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



x_offset = 170
height = 150
draw_speed = 6000
targetWidth = 25
lineSpacing = .5


myRobot.drawBitmap('skull.jpg', targetWidth, lineSpacing, x_offset, height, draw_speed)



# Dock the arm before exit
myRobot.goto(225, 0, 150, 6000)
myRobot.goto(130, 0, 90, 6000)
myRobot.goto(97, 0, 30, 6000)
