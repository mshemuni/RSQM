# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:53:37 2019

@author: msh
"""

from time import sleep

import RPi.GPIO as GPIO

from . import env

class reset():
    def __init__(self, verb=True, debugger):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.pin_list = {"run": 3, "stop": 5, "home": 7}
        
    def do(self):
         GPIO.setmode(GPIO.BOARD)
         GPIO.setwarnings(False)
         for action in self.pin_list:
             GPIO.setup(self.pin_list[action], GPIO.OUT)
             GPIO.output(self.pin_list[action], True)
        
class rotate():
    def __init__(self, verb=True, debugger):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.pin_list = {"run": 3, "stop": 5, "home": 7}
        
    def pulse(self, pin_number):
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(pin_number, GPIO.OUT)
            GPIO.output(pin_number, True)
            sleep(0.2)
            GPIO.output(pin_number, False)
            sleep(1)
            GPIO.output(pin_number, True)
        except Exception as e:
            self.logger.log(e)
        
    def one_step(self):
        try:
            self.pulse(self.pin_list["run"])
        except Exception as e:
            self.logger.log(e)
            
    def STOP(self):
        try:
            self.pulse(self.pin_list["stop"])
        except Exception as e:
            self.logger.log(e)
            
    def home(self):
        try:
            self.pulse(self.pin_list["home"])
        except Exception as e:
            self.logger.log(e)
        