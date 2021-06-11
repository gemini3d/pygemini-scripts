#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 10:34:45 2021

@author: zettergm
"""

# imports
import gemini3d.read
from plotcurv import plotcurv3D
import numpy as np

# load some sample data (3D)
direc="~/simulations/raid/tohoku20113D_lowres_2Daxisneu/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,cfg["time"][-1])

# grid data
parm=np.array(dat["v1"])
plotcurv3D(xg,parm,cfg,lalt=128,llon=128,llat=128)

