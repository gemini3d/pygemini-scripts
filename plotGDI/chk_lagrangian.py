#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 19:40:12 2023

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interpn

flagpot=True           # plot potential
flagframeshift=True    # shift quantities into same FOR

# information about the ExB drift (or grid drift as the case may be)
v2grid=900
v3grid=0
x20=-200e3

parmlbl="ne"
altref=[90e3,115e3,300e3,600e3,800e3]


# Read data
if not ("xg" in locals()):
    print("Reloading data...")
#    direc="~/simulations/ssd/200km_lagrangian8/"
#    direc2="~/simulations/ssd/200km_eulerian3/"
    direc="~/simulations/ssd/200km_lagrangian_symmsplit_planar/"
    direc2="~/simulations/ssd/200km_eulerian_symmsplit_planar/"
    cfg=gemini3d.read.config(direc)
    xg=gemini3d.read.grid(direc)
    x=xg["x2"][2:-2]
    y=xg["x3"][2:-2]
    z=xg["x1"][2:-2]
    xg2=gemini3d.read.grid(direc2)
    x2=xg2["x2"][2:-2]
    y2=xg2["x3"][2:-2]
    z2=xg2["x1"][2:-2]
    it=20
    #dat=gemini3d.read.frame(direc,cfg["time"][it],var=parmlbl)
    #dat2=gemini3d.read.frame(direc2,cfg["time"][it],var=parmlbl)   
    dat=gemini3d.read.frame(direc,cfg["time"][it])
    dat2=gemini3d.read.frame(direc2,cfg["time"][it])


# Apply FOR xform by shifting the Eulerian coordinates
print("Interpolating parameter of interest to a common grid...")
dataplot=np.array(dat[parmlbl])
dataplot2=np.array(dat2[parmlbl])
t=(cfg["time"][it]-cfg["time"][0]).total_seconds()
x2shift=x2-v2grid*t-x20
y2shift=y2-v3grid*t
[Z,X,Y]=np.meshgrid(np.array(z),np.array(x),np.array(y),indexing="ij")   # interpolation sites are based on Lagrangian grid
srcpoints=(np.array(z),np.array(x2shift),np.array(y2shift))
targetpoints=(Z.flatten(order="F"), X.flatten(order="F"), Y.flatten(order="F"))
dataplot2interp=interpn(srcpoints,dataplot2,targetpoints,bounds_error=False,fill_value=np.nan)
dataplot2interp=dataplot2interp.reshape(dataplot.shape,order="F")
    

# Compare the requested parameter
plt.subplots(len(altref),3,dpi=150)
for ialt in range(0,len(altref)):
    iz=np.argmin(abs(z-altref[ialt]))
    plt.subplot(len(altref),3,3*ialt+1)
    plt.pcolormesh(x,y,dataplot[iz,:,:].transpose())
    plt.colorbar()
    if (ialt==0):
        plt.title(direc)
    iz2=np.argmin(abs(z2-altref[ialt]))
    plt.subplot(len(altref),3,3*ialt+2)
    plt.pcolormesh(x2,y2,dataplot2interp[iz2,:,:].transpose())
    plt.colorbar()
    if (ialt==0):
        plt.title(direc2)
    plt.subplot(len(altref),3,3*ialt+3)
    plt.pcolormesh(x,y,(dataplot[iz,:,:]-dataplot2interp[iz2,:,:]).transpose())
    plt.colorbar()
    if (ialt==0):
        plt.title(parmlbl+" "+str(cfg["time"][it]))
    plt.show()


# Interpolate potential as well
print("Resampling potential pattern...")
Phiplot=np.array(dat["Phitop"])
Phiplot2=np.array(dat2["Phitop"])
[X,Y]=np.meshgrid(np.array(x),np.array(y),indexing="ij")   # interpolation sites are based on Lagrangian grid
srcpoints=(np.array(x2shift),np.array(y2shift))
targetpoints=(X.flatten(order="F"), Y.flatten(order="F"))
Phiplot2interp=interpn(srcpoints,Phiplot2,targetpoints,bounds_error=False,fill_value=np.nan)
Phiplot2interp=Phiplot2interp.reshape(Phiplot.shape,order="F")


# Also compare potential solutions
if flagpot: 
    plt.subplots(1,3,dpi=150)
    plt.subplot(1,3,1)
    plt.pcolormesh(Phiplot)
    plt.colorbar()
    plt.title(direc)
    plt.subplot(1,3,2)
    plt.pcolormesh(Phiplot2interp)
    plt.colorbar()
    plt.title(direc2)
    plt.subplot(1,3,3)
    plt.pcolormesh(Phiplot-Phiplot2interp)
    plt.colorbar()
    plt.title(parmlbl+" "+str(cfg["time"][it]))
    plt.show()


# # check source terms and potential solves for each
# lx=xg["lx"]
# lxtwo=xg2["lx"]

# fname="/Users/zettergm/simulations/ssd/200km_lagrangian5/potdebug.dat"
# fdata=np.fromfile(fname,dtype="float64",count=lx[1]*lx[2]*2)
# fdata=fdata.reshape((2,lx[1],lx[2]))
# srcterm=fdata[0,:,:]
# Phislab=fdata[1,:,:]

# fname2="/Users/zettergm/simulations/ssd/200km_eulerian3/potdebug.dat"
# fdata2=np.fromfile(fname2,dtype="float64",count=lxtwo[1]*lxtwo[2]*2)
# fdata2=fdata2.reshape((2,lxtwo[1],lxtwo[2]))
# srcterm2=fdata2[0,:,:]
# Phislab2=fdata2[1,:,:]


# # plot debug info
# plt.subplots(2,2,dpi=150)
# plt.subplot(2,2,1)
# plt.pcolormesh(srcterm)
# plt.colorbar()

# plt.subplot(2,2,2)
# plt.pcolormesh(Phislab)
# plt.colorbar()

# plt.subplot(2,2,3)
# plt.pcolormesh(srcterm2)
# plt.colorbar()

# plt.subplot(2,2,4)
# plt.pcolormesh(Phislab2)
# plt.colorbar()

