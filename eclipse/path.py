#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 12:51:46 2023

@author: zettergm
"""

import numpy as np

# beginning and ending location of eclipse
glon=np.array([360-147,360-29])
glat=np.array([49,-5])
UT=np.array([16+12/60, 19+46/60])*3500

# assume annularity forms a straight line (ridiculous)
slopelat=np.diff(glat)/np.diff(UT)
slopelon=np.diff(glon)/np.diff(UT)

