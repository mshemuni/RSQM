# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:02:43 2019

@author: msh
"""

from sqm import data

sdh = data.handle("com4", verb=True, debugger=True)
data_mean = sdh.read()
print(data_mean)