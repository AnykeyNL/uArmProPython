
# uArmProPython
uArm Swift Pro robot arm Python library and example code snippets. Based on a fork from Richar Gasthaagen's repository

Note 1: The svgo and convert binaries are external to Python. Meaning, you need to install imagemagick and node.js on your system (e.g., sudo apt-get install imagemagick npm) and the svgo command for node.js (npg install -g svgo). These functionalities were tested on Kubuntu Linux 16.04. Installation instructions for Windows can be found in the file uArmLaser_windows_guide.txt.

Please, be careful with the laser. Don't blind yourself or burn your house down :)

If you create something cool with these functions, please show me too :) Primarily I'm just curious, and also seeing other people's work might give ideas on how to improve the code. So, don't hesitate to drop me an email: ossi.lehtinen@gmail.com









The original readme:

# uArmProPython
Python Library for the uArm swift Pro robot arm

Created by: Richard Garsthagen - the.anykey@gmail.com
V0.2 - June 2017 - Still under development !!

See the 2 examples files on how to use the library.

Supports:
- Connecting to uArm swift Pro and setting the mode
- Basic move command in absolute coordinates
- Control single or multiple robots at a time. Support aSync mode for multiple robots.
- Turn on/off pump
- Drawing a circle

More to follow :-)
