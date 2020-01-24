# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 09:45:24 2019

@author: mshem
"""
from datetime import datetime
from datetime import timedelta

from math import floor
from math import log10
from math import pow as power

from matplotlib import pyplot as plt

from numpy import float64 as f64
from numpy import asarray as ar
from numpy import dstack
from numpy import unique
from numpy import cos
from numpy import sin
from numpy import arccos
from numpy import ones
from numpy import ceil
from numpy import mean
from numpy import std
from numpy import deg2rad
from numpy import rad2deg


from astropy.stats import histogram as hist

from astropy import units

from astropy.io import fits as fts
from astropy.table import Table
from astropy.coordinates import EarthLocation
from astropy.coordinates import SkyCoord
from astropy.coordinates import AltAz
from astropy.coordinates import Angle

from astropy.coordinates import get_sun
from astropy.coordinates import get_moon

from astropy.time import Time as tm

from astroplan import Observer
from astroplan import download_IERS_A

from skimage.color import rgb2gray as r2g
from skimage.feature import hog as the_hog
from skimage.exposure import rescale_intensity as ri

from sep import extract
from sep import Background

from cv2 import resize as cvresize

class SQM:
    def __init__(self, logger):
        self.logger = logger
        
    def mag_calc(self, mag):
        try:
            return 7.93 - 5 * (log10(power(10, (4.316 - (mag/5)))+ 1))
        except Exception as excpt:
            self.logger.log(excpt)

class Update:
    """Updates modules"""
    def __init__(self, logger):
        self.logger = logger

    def astroplan(self):
        """Updates astropy"""
        try:
            download_IERS_A()
        except Exception as excpt:
            self.logger.log(excpt)

class Time:
    """Time Class"""
    def __init__(self, logger):
        self.logger = logger
        
    def now(self, utc=True):
        try:
            if utc:
                return tm(datetime.utcnow(), scale='utc')
            else:
                return tm(datetime.now())
        except Exception as excpt:
            self.logger.log(excpt)

    def str2time(self, time, FORMAT='%Y-%m-%dT%H:%M:%S.%f'):
        """Converts string to time object"""
        try:
            datetime_object = datetime.strptime(time, FORMAT)
            return datetime_object
        except Exception as excpt:
            self.logger.log(excpt)

    def time_diff(self, time, time_offset=-3, offset_type="hours"):
        """Time difference calculator"""
        if time is not None and time_offset is not None:
            try:
                if "HOURS".startswith(offset_type.upper()):
                    return time + timedelta(hours=time_offset)
                elif "MINUTES".startswith(offset_type.upper()):
                    return time + timedelta(minutes=time_offset)
                elif "SECONDS".startswith(offset_type.upper()):
                    return time + timedelta(seconds=time_offset)

            except Exception as excpt:
                self.logger.log(excpt)
        else:
            self.logger.log("False Type: One of the values is not correct")

    def jd(self, utc):
        """JD calculator"""
        try:
            t = tm(utc, scale='utc')
            return t.jd
        except Exception as excpt:
            self.logger.log(excpt)

    def jd_r(self, jd):
        """JD to Time calculator"""
        try:
            t = tm(jd, format='jd', scale='tai')
            return t.to_datetime()
        except Exception as excpt:
            self.logger.log(excpt)


class TimeCalc(Time):
    def __init__(self, logger, site):
        super().__init__(logger)
        self._obs_ = site.__observer__()

    def __which_corrector__(self, which):
        if "PREVIOUS".startswith(which.upper()):
            return "previous"
        elif "CLOSEST".startswith(which.upper()):
            return "nearest"
        else:
            return "next"

    def __utc_corrector__(self, utc):
        if utc is None:
            return datetime.now()
        else:
            return utc

    def is_night(self, utc):
        try:
            return self._obs_.is_night(tm(utc))
        except Exception as excpt:
            self.logger.log(excpt)

    def midnight(self, utc, jd=False):
        try:
            if jd:
                return self._obs_.midnight(tm(utc)).jd
            else:
                return self._obs_.midnight(tm(utc)).datetime
        except Exception as excpt:
            self.logger.log(excpt)

    def sun_rise_time(self, utc, which="next", jd=False):
        try:
            which = self.__which_corrector__(which)
            sun_rise = self._obs_.sun_rise_time(tm(utc), which=which)
            if jd:
                return sun_rise.jd
            else:
                return sun_rise.datetime
        except Exception as excpt:
            self.logger.log(excpt)

    def sun_set_time(self, utc, which="next", jd=False):
        try:
            which = self.__which_corrector__(which)
            sun_set = self._obs_.sun_set_time(tm(utc), which=which)
            if jd:
                return sun_set.jd
            else:
                return sun_set.datetime
        except Exception as excpt:
            self.logger.log(excpt)

    def moon_rise_time(self, utc, which="next", jd=False):
        try:
            which = self.__which_corrector__(which)
            moon_rise = self._obs_.moon_rise_time(tm(utc))
            if jd:
                return moon_rise.jd
            else:
                return moon_rise.datetime
        except Exception as excpt:
            self.logger.log(excpt)

    def moon_set_time(self, utc, which="next", jd=False):
        try:
            which = self.__which_corrector__(which)
            moon_set = self._obs_.moon_set_time(tm(utc), which=which)
            if jd:
                return moon_set.jd
            else:
                return moon_set.datetime
        except Exception as excpt:
            self.logger.log(excpt)

    def twilight_morning(self, utc, tp="ASTRONOMICAL", which="next", jd=False):
        try:
            which = self.__which_corrector__(which)
            if "CIVIL".startswith(tp.upper()):
                ret = self._obs_.twilight_morning_civil(
                    tm(utc), which=which)
            elif "NAUTICAL".startswith(tp.upper()):
                ret = self._obs_.twilight_morning_nautical(
                    tm(utc), which=which)
            else:
                ret = self._obs_.twilight_morning_astronomical(
                    tm(utc), which=which)

            if jd:
                return ret.jd
            else:
                return ret.datetime

        except Exception as excpt:
            self.logger.log(excpt)

    def twilight_evening(self, utc, tp="ASTRONOMICAL", which="next", jd=False):
        try:
            which = self.__which_corrector__(which)
            if "CIVIL".startswith(tp.upper()):
                ret = self._obs_.twilight_evening_civil(
                    tm(utc), which=which)
            elif "NAUTICAL".startswith(tp.upper()):
                ret = self._obs_.twilight_evening_nautical(
                    tm(utc), which=which)
            else:
                ret = self._obs_.twilight_evening_astronomical(
                    tm(utc), which=which)

            if jd:
                return ret.jd
            else:
                return ret.datetime
        except Exception as excpt:
            self.logger.log(excpt)
            
    def day_part(self, utc, gap=30):
        try:
            jd_gap = 0.000694444 * gap
            jd = self.jd(utc)
            
            floor_jd = floor(jd)
            floor_date = self.jd_r(floor_jd)

            twi_start_jd = self.twilight_evening(floor_date,
                                                 which="NEXT", jd=True)
            twi_end_jd = self.twilight_morning(floor_date,
                                               which="NEXT", jd=True)
            if twi_start_jd + jd_gap < jd and jd < twi_end_jd + jd_gap:
                return 1
            
            if twi_start_jd - jd_gap > jd or jd > twi_end_jd - jd_gap:
                return 0
            
            return -1
            
        except Exception as excpt:
            self.logger.log(excpt)


class Coordinates:
    """Coordinate Class"""
    def __init__(self, logger):
        self.logger = logger

    def create_angle(self, angle):
        """Convert String to angle"""
        try:
            return Angle(angle)
        except Exception as excpt:
            self.logger.log(excpt)
    def alt_az(self, alt, az):
        try:
            alt = self.create_angle(alt)
            az = self.create_angle(az)
            return SkyCoord(AltAz(az, alt))
        except Exception as excpt:
            self.logger.log(excpt)
            
    def ra_dec(self, ra, dec):
        try:
            ra = self.create_angle(ra)
            dec = self.create_angle(dec)
            return SkyCoord(ra=ra, dec=dec)
        except Exception as excpt:
            self.logger.log(excpt)
            
    def distance(self, coord1, coord2):
        try:
            try:
                c1_ver = coord1.alt
                c1_hor = coord1.az
                
                c2_ver = coord2.alt
                c2_hor = coord2.az
            except:
                c1_ver = coord1.dec
                c1_hor = coord1.ra
                
                c2_ver = coord2.dec
                c2_hor = coord2.ra
            
            return rad2deg(arccos(sin(deg2rad(c1_ver)) * sin(deg2rad(c2_ver))
                                  + cos(deg2rad(c1_ver)) * cos(deg2rad(c2_ver))
                                  * cos((deg2rad(c1_hor - c2_hor)))))
            
        except Exception as excpt:
            self.logger.log(excpt)


class Site:
    """Site Class"""
    def __init__(self, logger, lati, long, alti, name="Obervatory"):
        self.logger = logger
        self._lati_ = lati
        self._long_ = long
        self._alti_ = alti
        self._name_ = name
        self.site = self.create()
        
    def __str__(self):
        return "An EarthLocation object at {}, {}".format(self._lati_.degree, self._long_.degree)
        
    def __repr__(self):
        return self.site

    def __observer__(self):
        try:
            return Observer(location=self.site, name=self._name_)
        except Exception as excpt:
            self.logger.log(excpt)

    def create(self):
        """Create site"""
        try:
            s = EarthLocation(lat=self._lati_, lon=self._long_,
                              height=self._alti_ * units.m)
            return s
        except Exception as excpt:
            self.logger.log(excpt)

    def update(self, lati, long, alti):
        """Update Site"""
        try:
            self.site = EarthLocation(lat=lati, lon=long,
                                      height=alti * units.m)
        except Exception as excpt:
            self.logger.log(excpt)

    def altaz(self, obj, utc):
        """Return AltAz for a given object and time for this site"""
        try:
            frame_of_sire = AltAz(obstime=utc, location=self.site)
            object_alt_az = obj.obj.transform_to(frame_of_sire)
            return object_alt_az
        except Exception as excpt:
            self.logger.log(excpt)


class Obj:
    """Object Class"""
    def __init__(self, logger, ra, dec):
        self.logger = logger
        self._ra_ = ra
        self._dec_ = dec
        self.obj = self.create()
        
    def __str__(self):
        return "A SkyCoord object at {}, {}".format(self.obj.ra.degree, self.obj.dec.degree)
        
    def __repr__(self):
        return self.obj

    def create(self):
        """Create Object"""
        try:
            return SkyCoord(ra=self._ra_, dec=self._dec_)
        except Exception as excpt:
            self.logger.log(excpt)

    def update(self, ra, dec):
        """Update Object"""
        try:
            self.obj = SkyCoord(ra=ra, dec=dec)
        except Exception as excpt:
            self.logger.log(excpt)

    def altaz(self, site, utc):
        """Return AltAz for a site object and time for this object"""
        try:
            frame_of_sire = AltAz(obstime=utc, location=site.site)
            object_alt_az = self.obj.transform_to(frame_of_sire)
            return object_alt_az
        except Exception as excpt:
            self.logger.log(excpt)


class Sun(Obj):
    def __init__(self, logger, time):
        self.logger = logger
        self._time_ = time
        self.obj = self.create()

    def create(self):
        try:
            return get_sun(tm(self._time_, scale='utc'))
        except Exception as excpt:
            self.logger.log(excpt)

    def update(self, time):
        try:
            return get_sun(tm(time, scale='utc'))
        except Exception as excpt:
            self.logger.log(excpt)


class Moon(Obj):
    def __init__(self, logger, time):
        self.logger = logger
        self._time_ = time
        self.obj = self.create()

    def create(self):
        try:
            return get_moon(tm(self._time_, scale='utc'))
        except Exception as excpt:
            self.logger.log(excpt)

    def update(self, time):
        try:
            return get_moon(tm(time, scale='utc'))
        except Exception as excpt:
            self.logger.log(excpt)
