# uArm Swift Pro - Python Library
# Created by: Richard Garsthagen - the.anykey@gmail.com
# V0.3 - June 2018 - Still under development
#
# Support for the old and new firmware

import serial
import time
import protocol_swiftpro as protocol
import threading
import sys
import math
from math import pi


class robot:
    serid = 100
    num_of_robots = 0
    baud = 115200
    serial_timeout = 1
    connect_timeout = 1
    debug = False
    baseThreadCount = threading.activeCount()
    delay_after_move = 0.1
    version = 0
    threads = 0
    X = float(200)
    Y = float(0)
    Z = float(100)
        
    def __init__(self, serialport, version):
        self.serialport = serialport
        self.connected = False
        robot.num_of_robots += 1
        self.moving = False
        self.pumping = False
        self.limit = False
        self.version = version

    def connect(self):
        try:
            if (self.debug): print ("trying to connect to: " + self.serialport)
            self.ser = serial.Serial(self.serialport, 115200, timeout=1)
            time.sleep(self.connect_timeout)
            
            Ready = False
            while (not Ready):
                line = self.ser.readline()
                if (self.debug): print (line)
                
                if line.startswith("@5") and self.version ==0 :
                    Ready = True
                    self.connected = True
                    if (self.debug): print ("Connected!")
                    return True

                if line.startswith("@1") and self.version == 1 :
                    Ready = True
                    self.connected = True
                    if (self.debug): print ("Connected!")
                    return True
            line = self.ser.readline() # Ignore if @6 response is given
            if line.startswith("@6 N0 V1"):
                self.limit = True
            if line.startswith("@6 N0 V0"):
                self.limit = False
            
                        
        except Exception as e:
            if (self.debug): print ("Error trying to connect to: " + self.serialport + " - " + str(e))
            self.connected = False
            return False

    def disconnect(self):
        if self.connected:
            if (self.debug): print ("Closing serial connection")
            self.connected = False
            self.ser.close()
        else:
            if (self.debug): print ("Disconnected called while not connected")

    def sendcmd(self, cmnd, waitresponse):
        self.threads = self.threads + 1
        if (self.connected):
            id = self.serid
            self.serid += 1
            cmnd = "#{} {}".format(id,cmnd)
            cmndString = bytes(cmnd + "\n")
            if (self.debug): print ("Serial send: {}".format(cmndString))
            self.ser.write(cmndString)
            if (waitresponse):
                line = self.ser.readline()
                if (self.debug): print ("Serial received: {}".format(line))
                while line.find("$" + str(id)) == -1:
                    if line.startswith("@6 N0 V1"):
                        self.limit = True
                    if line.startswith("@6 N0 V0"):
                        self.limit = False
                    line = self.ser.readline()
                    if (self.debug): print ("Serial received: {}".format(line))
                if (self.debug): print ("Response {}".format(line))
                if line.find("X") != -1 and line.find("Y") != -1 and line.find("Z") != -1:
                    try:
                        rit, stat, X, Y, Z = line.split(" ")
                        self.X = float(X[1:])
                        self.Y = float(Y[1:])
                        self.Z = float(Z[1:])
                    except:
                        if (self.debug): print ("Incorrect coordinate response")
                if (self.moving):
                    self.moving = False
                    time.sleep(self.delay_after_move)
                self.threads = self.threads -1
                return line
        else:
            if (self.debug):
                print ("error, trying to send command while not connected")
                self.moving = False
                self.threads = self.threads -1

    def goto(self,x,y,z,speed):
        self.moving = True
        x = str(round(x, 2))
        y = str(round(y, 2))
        z = str(round(z, 2))
        s = str(round(speed, 2))
        if self.version == 0:
            cmd = protocol.SET_POSITION.format(x,y,z,s)
        if self.version == 1:
            cmd = protocol.SET_POSITION_L.format(x,y,z,s)
        self.sendcmd(cmd, True)
        self.moving = False

    def movedown(self,speed):
        self.moving = True
        z = str(round(-1, 2))
        s = str(round(speed, 2))
        cmd = protocol.SET_POSITION_RELATIVE.format(0,0,z,s)
        self.sendcmd(cmd, True)
        self.moving = False

    def async_goto(self,x,y,z, speed):
        self.moving = True
        t = threading.Thread( target=self.goto , args=(x,y,z,speed) )
        while self.threads != 0:
            time.sleep(0.05)
        t.start()

    def get_coor(self):
        cmd= protocol.GET_COOR
        self.sendcmd(cmd, True)
        
    def pump(self, state):
        self.pumping = state
        cmd = protocol.SET_PUMP.format(int(state))
        self.sendcmd(cmd,True)

    def mode(self, modeid):
        # 0= Normal
        # 1= Laser
        # 2= 3D Printer
        # 3= Universal holder
        cmd = protocol.SET_MODE.format(modeid)
        self.sendcmd(cmd,True)

    def motors_on(self, state):
        if state == True:
            # Need firmware 4.1.1 or higher!
            cmd= protocol.ATTACH_MOTORS
            self.sendcmd(cmd, True)   
        if state == False:
            cmd= protocol.DETACH_MOTORS
            self.sendcmd(cmd, True)
            
    @staticmethod
    def PointsInCircum(r,n):
        return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in xrange(0,n+1)]


    def drawCircle(self, centerX, centerY, Radius, Resolution, Speed, DrawingHeight, StartFinishedHeight):
        if (Resolution < 4):
            #ignore drwaing circle, to low resoution
            if (self.debug): print ("Ignoring drwaing circle, to low resolution requested")
            return
        if (self.debug): print ("Drwaing circle of {} radius in {} steps".format(Radius,Resolution))
        offsetx = centerX
        offsety = centerY 
        c = self.PointsInCircum(Radius,Resolution)
        bx,by = c[0]
        self.goto(offsetx+bx,offsety+by,StartFinishedHeight,Speed)

        for p in range(0,Resolution):
            x,y = c[p]
            self.goto(offsetx+x,offsety+y,DrawingHeight,Speed)

        self.goto(offsetx+bx,offsety+by,DrawingHeight,Speed)
        time.sleep(0.5)
        self.goto(offsetx+bx,offsety+by,StartFinishedHeight,Speed)

        
        
            

            
        

        

        



        

        
            
            
        







