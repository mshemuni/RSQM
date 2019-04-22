# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 12:15:51 2018

@author: mshem
"""

from math import log10
from math import pow as power

from datetime import datetime
from datetime import timedelta

from astropy.time import Time
from . import env

class sqm():
    def __init__(self, verb=False, debugger=False):
        self.verb = verb
        self.debugger = debugger
    
    def mag_calc(self, mag):
        nmag = 7.93 - 5 * (log10(power(10, (4.316 - (mag/5)))+ 1))
        return(nmag)

class TimePython():
    def __init__(self, verb=False, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        
    def doy(self, date):
        return(int(date.strftime('%j')))
        
    def doy_j(self, jd):
        date = self.jd_r(jd)
        return(int(date.strftime('%j')))
        
    def str_to_time(self, date):
        """Returns a date object from string.
        Accepted time formats: ['YYYY-mm-ddTHH:MM:SS', 'YYYY-mm-dd HH:MM:SS']"""
        self.logger.log("Converting date({}) to date object".format(date))
        if self.logger.not_none(date):
            if "T" in date:
                frmt = '%Y-%m-%dT%H:%M:%S'
                
            elif " " in date:
                frmt = '%Y-%m-%d %H:%M:%S'
            else:
                self.logger.log("Unknown date format")
                frmt = None
            
            if self.logger.not_none(frmt):
                try:
                    datetime_object = datetime.strptime(date, frmt)
                    return(datetime_object)
                except Exception as e:
                    self.logger.log(e)
        else:
            self.logger.log("False Type: The value is not date")
                    
    def time_diff(self, time, time_offset=3, offset_type="hours"):
        """Returns new time object with added offset to given time object"""
        self.logger.log("Getting time({}) diff".format(time))
        if self.logger.not_none(time) or self.logger.not_none(time_offset):
            try:
                if "HOURS".startswith(offset_type.upper()):
                    ret = time + timedelta(hours=time_offset)
                elif "MINUTES".startswith(offset_type.upper()):
                    ret = time + timedelta(minutes=time_offset)
                elif "SECONDS".startswith(offset_type.upper()):
                    ret = time + timedelta(seconds=time_offset)
                elif "DAYS".startswith(offset_type.upper()):
                    ret = time + timedelta(days=time_offset)
                elif "MILLISECONDS".startswith(offset_type.upper()):
                    ret = time + timedelta(milliseconds=time_offset)
                else:
                    self.logger.log("Unknown time offset type")
                    ret = None
                    
                return(ret)
            except Exception as e:
                self.logger.log(e)
        else:
            self.logger.log("False Type: The value is not time or int")
            
    def local_to_utc(self, time, offset=3):
        """Returns UTC from local time"""
        self.logger.log("Getting UTC for local time({})".format(time))
        if self.logger.not_none(time) or self.logger.not_none(offset):
            try:
                ret = self.time_diff(time, time_offset=offset,
                                     offset_type="HOURS")
                return(ret)
            except Exception as e:
                self.logger.log(e)
        else:
            self.logger.log("False Type: The value is not time or int")
            
    def jd(self, utc):
        """Returns Modified Julian Date calculated from given UTC"""
        self.logger.log("Calculating JD for UTC time({})".format(utc))
        if self.logger.not_none(utc):
            try:
                ret = Time(utc, scale='utc')
                return(ret.jd)
            except Exception as e:
                self.logger.log(e)
        else:
            self.logger.log("False Type: The value is not date")
            
    def mjd(self, utc):
        """Returns Modified Julian Date (JD - 2400000.5) calculated from given UTC"""
        self.logger.log("Calculating MJD for UTC time({})".format(utc))
        if self.logger.not_none(utc):
            try:
                ret = Time(utc, scale='utc')
                return(ret.mjd)
            except Exception as e:
                self.logger.log(e)
        else:
            self.logger.log("False Type: The value is not date")
            
    def jd_r(self, jd):
        """Calculates time from jd"""
        try:
            self.logger.log("Calculating timestamp for JD({})".format(jd))
            t = Time(jd, format='jd', scale='tai')
            return(t.to_datetime())
        except Exception as e:
            self.logger.log(e)