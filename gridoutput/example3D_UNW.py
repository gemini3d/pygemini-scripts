#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 13:27:26 2022

Demonstrate native-to-native (e.g. UNW to UNW') interpolation of model output.

This uses lower-level utilities since there are no coordinate transformations
  involved; just interpolations.                                

@author: zettergm
"""

# imports
import gemini3d.read
from gemini3d.grid.gridmodeldata import interpmodeldata
import numpy as np
import matplotlib.pyplot as plt

# load example datafile and call interps
direc="~/simulations/GDI_LLpaper_trim"
print("...Reading config file...")
cfg=gemini3d.read.config(direc)
print("...Reading grid file...")
xg=gemini3d.read.grid(direc)
print("...Reading output frame file...")
dat=gemini3d.read.frame(direc,cfg["time"][-1])    # read final frame

# coordiantes and extents from grid dictionary
x1=xg["x1"][2:-2]    # UP:  remove ghost cells; we don't have output data for these
x2=xg["x2"][2:-2]    # NORTH
x3=xg["x3"][2:-2]    # WEST
x1min=np.min(x1)
x1max=np.max(x1)
x2min=np.min(x2)
x2max=np.max(x2)
x3min=np.min(x3)
x3max=np.max(x3)

# define a different set of points to interpolate to
lx1i=16
lx2i=512
lx3i=256
x1i=np.linspace(x1min,x1max,lx1i)
x2i=np.linspace(x2min,x2max,lx2i)
x3i=np.linspace(x3min,x3max,lx3i)
[X1i,X2i,X3i] = np.meshgrid(x1i,x2i,x3i, indexing="ij")    # assume these points represent a grid, flat list coudl also be used

# execute interpolation for some parameter
parmlbl="ne"
parmi=interpmodeldata(xg, x1, x2, x3, dat[parmlbl], X1i.ravel(), X2i.ravel(), X3i.ravel())    # wants a flat list as input
parmi=np.reshape(parmi,[lx1i,lx2i,lx3i])     # remake into a 3D gridded dataset

# just plot a random slice to make sure results are not garbage
plt.figure()
plt.pcolormesh(x3i,x2i,parmi[8,:,:],shading="auto")
plt.colorbar()
plt.xlabel("west dist. (m)")
plt.ylabel("north dist. (m)")
plt.show()
