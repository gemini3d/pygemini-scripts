#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 16:25:24 2022

Load gradient-drift instability simulation from Leslie Lamarches's paper and
grid it in geographic coordinates.  

@author: zettergm
"""

# imports
import gemini3d.read as read
import matplotlib.pyplot as plt
import os
import datetime

# location of simulation output
home=os.path.expanduser("~")
direc = home+"/simulations/raid/GDI_LLpaper_trim/"
cfg = read.config(direc)
xg = read.grid(direc)
parm="ne"
dat = read.frame(direc,time=datetime.datetime(2017,11,21,5,7,30))

# Cartesian coordinates (distance from RISR)
z=xg["x1"][2:-2]    # upward distance
x=xg["x2"][2:-2]    # northward distance
y=xg["x3"][2:-2]    # westward distance
ne=dat["ne"]

# location of RISR
glat=xg["glat"].mean()
glon=xg["glon"].mean()

# plot to check data
parmslice=ne[38,:,:]
plt.figure()
plt.pcolormesh(y/1e3,x/1e3,parmslice,shading="auto")
plt.colorbar()
plt.xlabel("westward dist. (km)")
plt.ylabel("northward dist. (km)")
plt.title("(glat,glon)=("+str(glat)+","+str(glon)+")")
plt.clim(0,4e11)
