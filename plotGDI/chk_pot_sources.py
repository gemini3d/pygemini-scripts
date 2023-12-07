#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:24:29 2023

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interpn


# information about the ExB drift (or grid drift as the case may be)
v2grid=900
v3grid=0


# Load the grid and configurations
direc="/Users/zettergm/simulations/ssd/200km_lagrangian_lowres4/"
direc2="/Users/zettergm/simulations/ssd/200km_eulerian_lowres4/"
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
fname=direc+"/Jdebug.dat"
fdata=np.fromfile(fname,dtype="float64",count=lx[0]*lx[1]*lx[2]*2)
fdata=fdata.reshape((lx[0],lx[1],lx[2],2),order="F")
J2=fdata[:,:,:,0]
J3=fdata[:,:,:,1]
fname2=direc2+"/Jdebug.dat"
fdata2=np.fromfile(fname2,dtype="float64",count=lxtwo[0]*lxtwo[1]*lxtwo[2]*2)
fdata2=fdata2.reshape((lxtwo[0],lxtwo[1],lxtwo[2],2),order="F")
J22=fdata2[:,:,:,0]
J32=fdata2[:,:,:,1]


# do the frame of reference shift for the Eulerian data
print("Interpolating parameter of interest to a common grid...")
J22plot=np.array(J22)
J32plot=np.array(J32)
t=2
x2shift=x2-v2grid*t
y2shift=y2-v3grid*t
[Z,X,Y]=np.meshgrid(np.array(z),np.array(x),np.array(y),indexing="ij")   # interpolation sites are based on Lagrangian grid
srcpoints=(np.array(z),np.array(x2shift),np.array(y2shift))
targetpoints=(Z.flatten(order="F"), X.flatten(order="F"), Y.flatten(order="F"))
J22plotinterp=interpn(srcpoints,J22plot,targetpoints,bounds_error=False,fill_value=np.nan)
J22plotinterp=J22plotinterp.reshape(J2.shape,order="F")
J32plotinterp=interpn(srcpoints,J32plot,targetpoints,bounds_error=False,fill_value=np.nan)
J32plotinterp=J32plotinterp.reshape(J3.shape,order="F")


# plot debug info
ialt=20;
plt.subplots(2,2,dpi=150)
plt.subplot(2,2,1)
plt.pcolormesh(x,y,J2[ialt,:,:].transpose())
plt.title("J2")
plt.colorbar()

plt.subplot(2,2,2)
plt.pcolormesh(x,y,J3[ialt,:,:].transpose())
plt.title("J3")
plt.colorbar()

plt.subplot(2,2,3)
plt.pcolormesh(x2,y2,J22plotinterp[ialt,:,:].transpose())
plt.colorbar()

plt.subplot(2,2,4)
plt.pcolormesh(x2,y2,J32plotinterp[ialt,:,:].transpose())
plt.colorbar()


plt.subplots(1,2,dpi=150)
plt.subplot(1,2,1)
plt.pcolormesh(x,y,(J2[ialt,:,:]-J22plotinterp[ialt,:,:]).transpose())
plt.title("dJ2")
plt.colorbar()

plt.subplot(1,2,2)
plt.pcolormesh(x,y,(J3[ialt,:,:]-J32plotinterp[ialt,:,:]).transpose())
plt.title("dJ3")
plt.colorbar()


