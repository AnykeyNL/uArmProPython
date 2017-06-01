# uArm Swift Pro - Python Library
# Created by: Richard Garsthagen - the.anykey@gmail.com
# V0.1 - June 2017 - Still under development

import serial
import time
import protocol_swiftpro as protocol
import threading
import sys


class robot:
    serid = 100
    num_of_robots = 0
    baud = 115200
    serial_timeout = 1
    connect_timeout = 1
    debug = False
    baseThreadCount = threading.activeCount()
    delay_after_move = 0.1
    
    def __init__(self, serialport):
        self.serialport = serialport
        self.connected = False
        robot.num_of_robots += 1
        self.moving = False
        self.pumping = False

    def connect(self):
        try:
            if (self.debug): print ("trying to connect to: " + self.serialport)
            self.ser = serial.Serial(self.serialport, 115200, timeout=1)
            time.sleep(self.connect_timeout)
            
            Ready = False
            while (not Ready):
                line = self.ser.readline()
                if (self.debug): print (line)
                if line.startswith("@5"):
                    Ready = True
                    self.connected = True
                    if (self.debug): print ("Connected!")
                    return True
            line = self.ser.readline() # Ignore if @6 response is given
            print (line)
                        
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
        if (self.connected):
            id = self.serid
            self.serid += 1
            cmnd = "#{} {}".format(id,cmnd)
            cmndString = bytes(cmnd + "\n")
            if (self.debug): print ("Serial send: {}".format(cmndString))
            self.ser.write(cmndString)
            if (waitresponse):
                line = self.ser.readline()
                while not line.startswith("$" + str(id)):
                    line = self.ser.readline()
                if (self.debug): print ("Response {}".format(line))
                if (self.moving):
                    self.moving = False
                    time.sleep(self.delay_after_move)
                return line
        else:
            if (self.debug):
                print ("error, trying to send command while not connected")
                self.moving = False

    def goto(self,x,y,z,speed):
        self.moving = True
        x = str(round(x, 2))
        y = str(round(y, 2))
        z = str(round(z, 2))
        s = str(round(speed, 2))
        cmd = protocol.SET_POSITION.format(x,y,z,s)
        self.sendcmd(cmd, True)

    def async_goto(self,x,y,z, speed):
        self.moving = True
        t = threading.Thread( target=self.goto , args=(x,y,z,speed) )
        t.start()

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

        

        



        

        
            
            
        







