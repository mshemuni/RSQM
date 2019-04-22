# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:10:13 2019

@author: msh
"""

import ephem

from . import env
from . import ast

class moon():
    def __init__(self, verb=False, debugger=False, lon = '39.7833', lat = '41.2333', elevation = 3170):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.atm = ast.TimePython(verb=self.verb, debugger=self.debugger)
        self.lon = lon
        self.lat = lat
        self.elevation = elevation
        
    def convert_sex_to_deg(self, angle):
        an = angle.split(":")
        if angle.startswith("-"):
            return(float(an[0]) - float(an[1])/60 - float(an[2])/3600)
        else:
            return(float(an[0]) + float(an[1])/60 + float(an[2])/3600)
        
    def coordinates(self, jd):
        site = ephem.Observer()
        site.lon = self.lon
        site.lat = self.lat
        site.elevation = self.elevation
        site.date = str(self.atm.jd_r(jd))
        the_object = ephem.Moon()
        the_object.compute(site)
        az = str(the_object.az)
        alt = str(the_object.alt)
        ret_az = self.convert_sex_to_deg(az)
        ret_alt = self.convert_sex_to_deg(alt)
        return(ret_alt, ret_az, int(ret_alt/abs(ret_alt)),the_object.phase, the_object.mag)
        
class sun():
    def __init__(self, verb=False, debugger=False, lon = '39.7833', lat = '41.2333', elevation = 3170):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.atm = ast.TimePython(verb=self.verb, debugger=self.debugger)
        self.lon = lon
        self.lat = lat
        self.elevation = elevation
        
    def convert_sex_to_deg(self, angle):
        an = angle.split(":")
        if angle.startswith("-"):
            return(float(an[0]) - float(an[1])/60 - float(an[2])/3600)
        else:
            return(float(an[0]) + float(an[1])/60 + float(an[2])/3600)
        
    def coordinates(self, jd):
        site = ephem.Observer()
        site.lon = self.lon
        site.lat = self.lat
        site.elevation = self.elevation
        site.date = str(self.atm.jd_r(jd))
        the_object = ephem.Sun()
        the_object.compute(site)
        az = str(the_object.az)
        alt = str(the_object.alt)
        ret_az = self.convert_sex_to_deg(az)
        ret_alt = self.convert_sex_to_deg(alt)
        return(ret_alt, ret_az, int(ret_alt/abs(ret_alt)),the_object.phase, the_object.mag)