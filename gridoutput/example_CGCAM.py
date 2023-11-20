#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 09:29:49 2023

@author: zettergm
"""

# imports
import gemini3d.read as read
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2geogcoords
import numpy as np
#import xarray

# load some sample data (3D)
direc = "~/simulations/ssd/CGCAM_NZv2/"
cfg = read.config(direc)
xg = read.grid(direc)
parm="ne"
dat0 = read.frame(direc, cfg["time"][0], var=parm)
dat = read.frame(direc, cfg["time"][32], var=parm)

# produce gridding datasets from model
#lalt=384; llon=128; llat=384;
lalt=384; llon=384; llat=384;

# regrid data in geographic
print("Sampling model results in geographic coords...")
galti, gloni, glati, parmgi = model2geogcoords(xg, 100*(dat[parm]-dat0[parm])/dat0[parm],
                                               lalt, llon, llat, wraplon=True)
if max(gloni)>360.0:
    gloni=gloni-360

# make a plot
# plt.figure(dpi=150)
# dataplot=np.squeeze(parmgi[:,llon//2,:])
# plt.pcolormesh(glati,galti,dataplot,shading="auto")
# plt.colorbar()
# plt.xlabel("latitude")
# plt.ylabel("altitude")

plt.figure(dpi=150)
ialt=np.argmin(abs(galti-300e3))
dataplot=np.squeeze(parmgi[ialt,:,:])
plt.pcolormesh(gloni,glati,dataplot.transpose(),shading="auto")
plt.colorbar()
plt.ylabel("latitude")
plt.xlabel("longitude")
plt.title("percent variation in $n_e$ @ 300 km altitude")

# plt.figure(dpi=150)
# dataplot=np.squeeze(parmgi[:,:,llat//2])
# plt.pcolormesh(gloni,galti,dataplot,shading="auto")
# plt.colorbar()
# plt.xlabel("longitude")
# plt.ylabel("altitude")