#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 09:57:23 2022

@author: zettergm
"""

# imports
import gemini3d.read as read
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2magcoords,model2geogcoords
import numpy as np
#import xarray

# load some sample data (3D)
#direc = "~/simulations/raid/tohoku20112D_medres/"
direc = "~/simulations/aurora_EISCAT3D_simple_wide/"
cfg = read.config(direc)
xg = read.grid(direc)
parm="ne"
dat = read.frame(direc, cfg["time"][-1], var=parm)

# produce gridding datasets from model
#lalt=384; llon=128; llat=384;
lalt=128; llon=128; llat=128;

# regrid data in geographic
print("Sampling in geographic coords...")
galti, gloni, glati, parmgi = model2geogcoords(xg, dat[parm], lalt, llon, llat, wraplon=True)

# regrid in geomagnetic
print("Sampling in geomagnetic coords...")
malti, mloni, mlati, parmmi = model2magcoords(xg, dat[parm], lalt, llon, llat)

# make a plot
plt.figure()
dataplot=np.squeeze(parmmi[:,llon//2,:])
plt.pcolormesh(dataplot,shading="auto")
plt.xlabel("latitude")
plt.ylabel("altitude")