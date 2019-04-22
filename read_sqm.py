# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:47:47 2019

@author: msh
"""
#Needed imports
from sqm import data
from sqm import rmt
from sqm import ast
from sqm import env
from sqm import time
from sqm import objects

#Constants for logging
deb = True
ver = True

#Port of SQM-lu
the_port = "com4"
number_of_samples_for_mean = 1000

#SQL variables
#Host: Ip or domain
host = "localhost"
#User name
user = "root"
#Password
passwd = ""
#Database name
database = "dummy"
#Single value table name
single_table = "sqm_single"
#Mean value table name
mean_table = "sqm"

#SQL fields for average values
fields_mean = ['sqm_id', 'start_jd', 'jd', 'end_jd', 'mag', 'sqm_mag_stdv',
               'sqm_mag', 'mag_stdv', 'temper', 'temper_stdv', 'moon_alt',
               'moon_az', 'moon_phase', 'moon_mag', 'moon_hori',
               'sample_number', 'valid_data']

#SQL fields for single value
fields_single = ['sqm_id', 'start_jd', 'jd', 'end_jd', 'mag', 'sqm_mag',
                 'temper', 'moon_alt', 'moon_az', 'moon_phase', 'moon_mag',
                 'moon_hori']

#Dummy variable. Will change with UPS condition
is_sqm_up = True

#Create a logger object
logger = env.Logger(verb=ver, debugger=deb)
#Create a time object
atm = ast.TimePython(verb=ver, debugger=deb)
#Create a moon object
moon = objects.moon(verb=ver, debugger=deb)

#Get Now(UTC)
now_utc = logger.time_stamp()
#Convert Not to JD
now_jd = atm.jd(now_utc)
#Get integer part of JD
int_now_jd = int(now_jd)
#Calculate UTC for integer JD
int_now_utc = atm.jd_r(int_now_jd)
#Create a site (for DAG) object
dag = time.astronomic(date=str(int_now_utc))
#Calculate Dusk Twilight for site
start_jd = atm.jd(dag.n_dusk_twilight_end())
#Calculate Dawn Twilight for site
end_jd = atm.jd(dag.n_dawn_twilight_start())

#Check if jd is between Dusk and Dawn
if not start_jd < now_jd < end_jd:
    #Create an SQL object
    sql = rmt.sql(host, user, passwd, database, port=3306,
                  verb=ver, debugger=deb)
    
    #Calculate moon coordinates
    the_moon = moon.coordinates(now_jd)
    
    #Create a data handler
    sdh = data.handle(the_port, verb=ver, debugger=deb)
    #Get average mesurments for 100 samples
    data_mean = sdh.mean_read(number_of_samples_for_mean)
    
    #Organize average data for fields
    #The data is: 'sqm_id', 'start_jd', 'jd', 'end_jd', 'mag', 'sqm_mag_stdv',
    #           'sqm_mag', 'mag_stdv', 'temper', 'temper_stdv', 'moon_alt',
    #           'moon_az', 'moon_phase', 'moon_mag', 'moon_hori',
    #           'sample_number', 'valid_data'
    sql_data_mean = [1, start_jd, data_mean[0], end_jd, data_mean[1],
                     data_mean[2], data_mean[3], data_mean[4], data_mean[5],
                     data_mean[6], the_moon[0],
                     the_moon[1], the_moon[3], the_moon[4], the_moon[2],
                     data_mean[7], data_mean[8]]
    
    #Insert data to corresponding table
    sql.insert(mean_table, fields_mean, [sql_data_mean])
    
    #Read a single value
    data_single = sdh.read()
    
    #Organize single data for fields
    #The data is: 'sqm_id', 'start_jd', 'jd', 'end_jd', 'mag', 'sqm_mag',
    #             'temper', 'moon_alt', 'moon_az', 'moon_phase', 'moon_mag',
    #             'moon_hori'
    sql_data_single = [1, start_jd, data_single[0], end_jd, data_single[1],
                       data_single[2], data_single[3],
                       the_moon[0], the_moon[1], the_moon[3], the_moon[4],
                       the_moon[2]]
    #Insert data to corresponding table
    sql.insert(single_table, fields_single, [sql_data_single])
    #Close sql connection
    sql.close()
    
    
else:
    #Log a line about no observation at given time
    logger.log("No observation at {}.".format(now_jd))