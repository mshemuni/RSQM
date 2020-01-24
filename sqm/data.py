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

from. import ast

class Handle:
    def __init__(self, logger, port):
        self.logger = logger
        self.port = port
        self.atm = ast.Time(self.logger)
        self.asm = ast.SQM(self.logger)
        
    def read(self):
        self.logger.log("Starting to read")
        try:
            self.con = self.connect()
            data = self._read_data_()
            self.close()
            return(data)
        except Exception as e:
            self.logger.log(e)
            self.close()
        
    def read_cont(self, number, interval):
        self.logger.log("Starting to read ({}) samples with ({}) interval".format(
                number, interval))
        try:
            data = []
            self.con = self.connect()
            for i in range(number):
                d = self._read_data_()
                if d is not None:
                    data.append(d)
                sleep(interval)
                
            self.close()
            data = ar(data)
            return(data)
        except Exception as e:
            self.logger.log(e)
            self.close()
        
    def mean_read(self, number):
        self.logger.log("Calculating mean and standard deviation of ({}) samples".format(number))
        try:
            data = []
            c = 0
            self.con = self.connect()
            for i in range(number):
                d = self._read_data_()
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
            return({"JD": mean_data[0], "Mag": mean_data[1], "STDV": stdv_mag,
                       "CMag": mean_data[2], "CSTDV": stdv_sqm_mag,
                       "Temperature": mean_data[3], "TemperatureSTDV": stdv_tmp,
                       "N": number, "Valid": c})
        except Exception as e:
            self.logger.log(e)
            self.close()
        
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
            
    def _read_data_(self):
        self.logger.log("Reading a line from device at ({})".format(self.port))
        if self.con is not None:
            try:
                self.con.write(str.encode("rx\n"))
                self.con.flush()
                tmp = str(self.con.readline()).split()
                utc = self.atm.now()
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
