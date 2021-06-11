#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 10:34:45 2021

@author: zettergm
"""

# imports
import gemini3d.read
from plotcurv import plotcurv2D
import numpy as np

# load some sample data (2D)
direc="~/simulations/raid/tohoku20112D_medres/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,cfg["time"][-1])

# grid data
parm=np.array(dat["v1"])
plotcurv2D(xg,parm,lalt=1024,llat=1024)

