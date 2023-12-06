#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:24:29 2023

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
import numpy as np

direc="~/simulations/ssd/200km_lagrangian5/"
direc2="~/simulations/ssd/200km_eulerian3/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
x=xg["x2"][2:-2]
y=xg["x3"][2:-2]
z=xg["x1"][2:-2]
cfg2=gemini3d.read.config(direc2)
xg2=gemini3d.read.grid(direc2)
x2=xg2["x2"][2:-2]
y2=xg2["x3"][2:-2]
z2=xg2["x1"][2:-2]

# check source terms and potential solves for each
lx=xg["lx"]
lxtwo=xg2["lx"]

fname="/Users/zettergm/simulations/ssd/200km_lagrangian5/Jdebug.dat"
fdata=np.fromfile(fname,dtype="float64",count=lx[0]*lx[1]*lx[2]*2)
fdata=fdata.reshape((lx[0],lx[1],lx[2],2),order="F")
J2=fdata[:,:,:,0]
J3=fdata[:,:,:,1]

fname2="/Users/zettergm/simulations/ssd/200km_eulerian3/Jdebug.dat"
fdata2=np.fromfile(fname2,dtype="float64",count=lxtwo[0]*lxtwo[1]*lxtwo[2]*2)
fdata2=fdata2.reshape((lxtwo[0],lxtwo[1],lxtwo[2],2),order="F")
J22=fdata2[:,:,:,0]
J32=fdata2[:,:,:,1]


# plot debug info
plt.subplots(2,2,dpi=150)
plt.subplot(2,2,1)
plt.pcolormesh(x,y,J2[20,:,:])
plt.colorbar()

plt.subplot(2,2,2)
plt.pcolormesh(x,y,J3[20,:,:])
plt.colorbar()

plt.subplot(2,2,3)
plt.pcolormesh(x2,y2,J22[20,:,:])
plt.colorbar()

plt.subplot(2,2,4)
plt.pcolormesh(x2,y2,J32[20,:,:])
plt.colorbar()