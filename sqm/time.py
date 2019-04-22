#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 12:38:30 2018

@author: msh
"""

import ephem

from datetime import datetime
import dateutil.parser

from . import env

class astronomic():
    def __init__(self, debugger=False, verb=False, lat='41.2333', lon='39.7833',
                 ele='3170', date=None, t_at_date=False, oname='DAG'):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.lat = lat
        self.lon = lon
        self.date = date
        self.ele = ele
        self.t_at_date = t_at_date
        self.oname = oname
        
    def obs_name(self):
        if self.oname == '':
            return("Observatory")
        else:
            return(self.oname)
        
    def time_formatter(self, in_time):
        try:
            if self.t_at_date:
                return(in_time.strftime("%Y-%m-%dT%H:%M:%S"))
            else:
                return(in_time.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            self.logger.log(e)
        
    def time_solver(self, in_time):
        try:
            the_date = dateutil.parser.parse(in_time)
            return(the_date)
        except Exception as e:
            self.logger.log(e)
    
    def angle_solver(self, in_angle):
        try:
            ang = float(in_angle)
            return(str(ang))
        except Exception as e:
            self.logger.log(e)
            
    def number_solver(self, in_number):
        try:
            ang = float(in_number)
            return(ang)
        except Exception as e:
            self.logger.log(e)
            
    def observat(self):
        self.__observatory__ = ephem.Observer()
        lat = self.angle_solver(self.lat)
        lon = self.angle_solver(self.lon)
        ele = self.number_solver(self.ele)
        if lat is not None:
            if lon is not None:
                if ele is not None:
                    self.__observatory__.lat = lat
                    self.__observatory__.lon = lon
                    self.__observatory__.date = self.date_solver()
                    self.__observatory__.elevation = ele
            else:
                self.logger.log("Abort. Cannot solve longitude")
        else:
            self.logger.log("Abort. Cannot solve latitude")
                
    def date_solver(self):
        if self.date is not None:
            dat = self.time_solver(self.date)
            if dat is not None:
                return(dat)
            else:
                self.logger.log("Cannot solve date. Calculation for NOW")
                return(datetime.now())
        else:
            self.logger.log("Date was None. Calculating for NOW")
            return(datetime.now())
            
    def nrising(self):
        try:
            sun = ephem.Sun()
            self.observat()
            rise = ephem.localtime(self.__observatory__.next_rising(sun))
            rise = self.time_formatter(rise)
            self.logger.log("Next sunrise in the {} will be @ '{}'".format(
                    self.obs_name(), rise))
            return(rise)
        except Exception as e:
            self.logger.log(e)
            
    def nsetting(self):
        try:
            sun = ephem.Sun()
            self.observat()
            sett = ephem.localtime(self.__observatory__.next_setting(sun))
            sett = self.time_formatter(sett)
            self.logger.log("Next sunrise in the {} will be @ '{}'".format(
                    self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def prising(self):
        try:
            sun = ephem.Sun()
            self.observat()
            rise = ephem.localtime(self.__observatory__.previous_rising(sun))
            rise = self.time_formatter(rise)
            self.logger.log("Previous sunrise in the {} will be @ '{}'".format(
                    self.obs_name(), rise))
            return(rise)
        except Exception as e:
            self.logger.log(e)
            
    def psetting(self):
        try:
            sun = ephem.Sun()
            self.observat()
            sett = ephem.localtime(self.__observatory__.previous_setting(sun))
            sett = self.time_formatter(sett)
            self.logger.log("Previous sunrise in the {} will be @ '{}'".format(
                    self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def m_nrising(self):
        try:
            moon = ephem.Moon()
            self.observat()
            rise = ephem.localtime(self.__observatory__.next_rising(moon))
            rise = self.time_formatter(rise)
            self.logger.log("Next moonrise in the {} will be @ '{}'".format(
                    self.obs_name(), rise))
            return(rise)
        except Exception as e:
            self.logger.log(e)
            
    def m_nsetting(self):
        try:
            moon = ephem.Moon()
            self.observat()
            sett = ephem.localtime(self.__observatory__.next_setting(moon))
            sett = self.time_formatter(sett)
            self.logger.log("Next moonrise in the {} will be @ '{}'".format(
                    self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def m_prising(self):
        try:
            moon = ephem.Moon()
            self.observat()
            rise = ephem.localtime(self.__observatory__.previous_rising(moon))
            rise = self.time_formatter(rise)
            self.logger.log("Previous moonrise in the {} will be @ '{}'".format(
                    self.obs_name(), rise))
            return(rise)
        except Exception as e:
            self.logger.log(e)
            
    def m_psetting(self):
        try:
            moon = ephem.Moon()
            self.observat()
            sett = ephem.localtime(self.__observatory__.previous_setting(moon))
            sett = self.time_formatter(sett)
            self.logger.log("Previous moonrise in the {} will be @ '{}'".format(
                    self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def n_dusk_twilight_start(self):
        try:
            sun = ephem.Sun()
            self.observat()
            self.__observatory__.horizon = '-12'
            sett = ephem.localtime(self.__observatory__.next_setting(
                    sun, use_center=True))
            sett = self.time_formatter(sett)
            self.logger.log("Next Dusk twilight in the {} will start @ '{}'".format(
                    self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def p_dusk_twilight_start(self):
        try:
            sun = ephem.Sun()
            self.observat()
            self.__observatory__.horizon = '-12'
            sett = ephem.localtime(self.__observatory__.previous_setting(
                    sun, use_center=True))
            sett = self.time_formatter(sett)
            self.logger.log("Previous Dusk twilight in the {} will start @ '{}'".format(
                    self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def n_dusk_twilight_end(self):
        try:
            sun = ephem.Sun()
            self.observat()
            self.__observatory__.horizon = '-18'
            sett = ephem.localtime(self.__observatory__.next_setting(
                    sun, use_center=True))
            sett = self.time_formatter(sett)
            self.logger.log("Next Dusk twilight in the {} will end @ '{}'".format(
                    self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def p_dusk_twilight_end(self):
        try:
            sun = ephem.Sun()
            self.observat()
            self.__observatory__.horizon = '-18'
            sett = ephem.localtime(self.__observatory__.previous_setting(
                    sun, use_center=True))
            sett = self.time_formatter(sett)
            self.logger.log(
                    "Previous Dusk twilight in the {} will end @ '{}'".format(
                            self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def n_dawn_twilight_start(self):
        try:
            sun = ephem.Sun()
            self.observat()
            self.__observatory__.horizon = '-12'
            sett = ephem.localtime(self.__observatory__.next_rising(
                    sun, use_center=True))
            sett = self.time_formatter(sett)
            self.logger.log(
                    "Next Dawn twilight in the {} will start @ '{}'".format(
                            self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def p_dawn_twilight_start(self):
        try:
            sun = ephem.Sun()
            self.observat()
            self.__observatory__.horizon = '-12'
            sett = ephem.localtime(self.__observatory__.previous_rising(
                    sun, use_center=True))
            sett = self.time_formatter(sett)
            self.logger.log(
                    "Previous Dawn twilight in the {} will start @ '{}'".format(
                            self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def n_dawn_twilight_end(self):
        try:
            sun = ephem.Sun()
            self.observat()
            self.__observatory__.horizon = '-18'
            sett = ephem.localtime(self.__observatory__.next_rising(
                    sun, use_center=True))
            sett = self.time_formatter(sett)
            self.logger.log("Next Dawn twilight in the {} will end @ '{}'".format(
                    self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)
            
    def p_dawn_twilight_end(self):
        try:
            sun = ephem.Sun()
            self.observat()
            self.__observatory__.horizon = '-18'
            sett = ephem.localtime(self.__observatory__.previous_rising(
                    sun, use_center=True))
            sett = self.time_formatter(sett)
            self.logger.log(
                    "Previous Dawn twilight in the {} will end @ '{}'".format(
                            self.obs_name(), sett))
            return(sett)
        except Exception as e:
            self.logger.log(e)