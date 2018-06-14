# uArmProPython
Python Library for the uArm swift Pro robot arm
Created by: Richard Garsthagen - the.anykey@gmail.com
V0.3 - June 2018 - Still under development !!

See the 2 examples files on how to use the library.

## Supports:
- Support for Firmware V4 and older firmwares
- Connecting to uArm swift Pro and setting the mode
- Basic move command in absolute coordinates
- Control single or multiple robots at a time. Support aSync mode for multiple robots.
- Turn on/off pump
- Drawing a circle

More to follow :-)

Using the initialization, you can specify the firmware of yor robot.
myRobot = uArmRobot.robot(serialport,1)

where 
0 = Firmware V1,v2,v3
1 = Firmware V4

