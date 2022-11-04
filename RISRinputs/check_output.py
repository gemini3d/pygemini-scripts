#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 17:20:51 2022

@author: zettergm
"""

# imports
import gemini3d.read
import matplotlib.pyplot as plt

# load simulations data
direc="~/simulations/GDI_RISR_MR_staging/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,time=cfg["time"][-1])

# grab Cartesian grid variables
x1=xg["x1"][2:-2]
x2=xg["x2"][2:-2]
x3=xg["x3"][2:-2]

# slice data
i1=23
Teslice=dat["Te"][i1,:,:]
neslice=dat["ne"][i1,:,:]

# plot
plt.figure(dpi=150)
plt.pcolormesh(x2,x3,Teslice)
plt.colorbar()
plt.show()

plt.figure(dpi=150)
plt.pcolormesh(x2,x3,neslice)
plt.colorbar()
plt.show()
