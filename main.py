# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:09:16 2019

@author: msh
"""

from sqm import env
from sqm import ast
from sqm import data

logger = env.Logger(blabla=True)

dh = data.Handle(logger, "com4")

coord = ast.Coordinates(logger)

longitude = coord.create_angle("39.7833 degree")
latitude = coord.create_angle("41.2333 degree")
elevation = 3170
dag = ast.Site(logger, latitude, longitude, elevation, name="DAG")

tim = ast.Time(logger)
tim_calc = ast.TimeCalc(logger, dag)

if not tim_calc.is_night(now := tim.now(utc=True)):
    data = dh.mean_read(10)
    moon = ast.Moon(logger, now)
    moon_alt_az = dag.altaz(moon, now)
    sqm_alt_az = coord.alt_az("30 degree", "180 degree")
    dist = coord.distance(moon_alt_az, sqm_alt_az)
    print(dist, data)
