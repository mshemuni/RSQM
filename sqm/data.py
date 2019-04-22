# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:09:16 2019

@author: msh
"""

import serial

from time import sleep

from numpy import array as ar
from numpy import mean 
from numpy import std

from . import env
from . import ast

class handle:
    def __init__(self, port, verb=True, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.port = port
        self.atm = ast.TimePython()
        self.asm = ast.sqm(verb=self.verb, debugger=self.debugger)
        
    def read(self):
        self.logger.log("Starting to read")
        try:
            self.con = self.connect()
            data = self.read_data()
            self.close()
            return(data)
        except Exception as e:
            self.logger.log(e)
        
    def read_cont(self, number, interval):
        self.logger.log("Starting to read ({}) samples with ({}) interval".format(
                number, interval))
        try:
            data = []
            self.con = self.connect()
            for i in range(number):
                d = self.read_data()
                if d is not None:
                    data.append(d)
                sleep(interval)
                
            self.close()
            data = ar(data)
            return(data)
        except Exception as e:
            self.logger.log(e)
        
    def mean_read(self, number):
        self.logger.log("Calculating mean and standard deviation of ({}) samples".format(number))
        try:
            data = []
            c = 0
            self.con = self.connect()
            for i in range(number):
                d = self.read_data()
                if d is not None:
                    data.append(d)
                    c += 1
                sleep(0.01)
                
            self.close()
            data = ar(data)
            mean_data = mean(data, axis=0)
            stdv_mag = std(data[:, 1])
            stdv_sqm_mag = std(data[:, 2])
            stdv_tmp = std(data[:, 3])
            return(ar([mean_data[0], mean_data[1], stdv_mag,
                       mean_data[2], stdv_sqm_mag,
                       mean_data[3], stdv_tmp, number, c]))
        except Exception as e:
            self.logger.log(e)
        
    def connect(self):
        self.logger.log("Creating a connetion to port ({})".format(self.port))
        try:
            ser = serial.Serial(port=self.port, baudrate=115200,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS, timeout=1)
            return(ser)
        except Exception as e:
            self.logger.log(e)
            
    def read_data(self):
        self.logger.log("Reading a line from device at ({})".format(self.port))
        if self.con is not None:
            try:
                self.con.write(str.encode("rx\n"))
                self.con.flush()
                tmp = str(self.con.readline()).split()
                utc = self.logger.time_stamp()
                mag = float(tmp[1].split(",")[0].replace("m", ""))
                sqm_mag = self.asm.mag_calc(mag)
                tempe = float(tmp[2].split("C")[0])
                return(ar([self.atm.jd(utc), mag, sqm_mag, tempe]))
            except Exception as e:
                self.logger.log(e)
            
    def close(self):
        self.logger.log("Closeing connection to port ({})".format(self.port))
        if self.con is not None:
            try:
                self.con.close()
            except Exception as e:
                self.logger.log(e)