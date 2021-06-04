#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 10:34:45 2021

@author: zettergm
"""

# imports
from gemini3d.grid.gridmodeldata import model2magcoords
import gemini3d.read
import matplotlib.pyplot as plt
import numpy as np

# load some sample data (3D)
direc="~/simulations/tohoku20112D_medres/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,cfg["time"][-1])

# grid data
parm=np.array(dat["v1"])
[alti,mloni,mlati,parmi]=model2magcoords(xg,parm,1024,1,1024)

# define slices indices
ilon=0

# plot various slices through the 3D domain
plt.figure()
plt.pcolormesh(mlati,alti/1e3,parmi[:,ilon,:])
plt.xlabel('mlat')
plt.ylabel('alt')
plt.colorbar()
