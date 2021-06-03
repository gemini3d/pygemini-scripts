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

# load some sample data
direc="~/simulations/tohoku20113D_lowres_2Daxisneu_CI/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,cfg["time"][-1])

# grid data
parm=np.array(dat["v1"])
[alti,mloni,mlati,parmi]=model2magcoords(xg,parm,256,256,256)

# define slices indices
altref=300e3
ialt=np.argmin(abs(alti-altref))
lonavg=cfg["sourcemlon"]
ilon=np.argmin(abs(mloni-lonavg))
latavg=cfg["sourcemlat"]
ilat=np.argmin(abs(mlati-latavg))

# plot various slices through the 3D domain
plt.subplots(1,3)

plt.subplot(1,3,1)
plt.pcolormesh(mloni,alti/1e3,parmi[:,:,ilat])
plt.xlabel('mlon')
plt.ylabel('alt')
plt.colorbar()

plt.subplot(1,3,2)
plt.pcolormesh(mloni,mlati,parmi[ialt,:,:].transpose())
plt.xlabel('mlon')
plt.ylabel('mlat')
plt.colorbar()

plt.subplot(1,3,3)
plt.pcolormesh(mlati,alti/1e3,parmi[:,ilon,:])
plt.xlabel('mlat')
plt.ylabel('alt')
plt.colorbar()
