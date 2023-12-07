#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 12:51:46 2023

@author: zettergm
"""

import numpy as np

def getreftime(targglon,targglat):  
    # beginning and ending location of eclipse
    glon=np.array([213,331])
    glat=np.array([49,-5])
    UT=np.array([56700, 69183.33])
    
    # assume annularity forms a straight line (ridiculous)
    slopelat=np.diff(glat)/np.diff(UT)
    slopelon=np.diff(glon)/np.diff(UT)
    
    # find max annularity time for a given location
    targtime_lat=UT[0]+(targglat-glat[0])/slopelat[0]
    targtime_lon=UT[0]+(targglon-glon[0])/slopelon[0]
    targtime=0.5*(targtime_lat+targtime_lon)     # just take an average
    
    return targtime


