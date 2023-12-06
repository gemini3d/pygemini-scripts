#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 19:40:12 2023

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
import numpy as np

flagpot=False

parmlbl="J2"
altref=[90e3,115e3,300e3,600e3,800e3]

if not ("xg" in locals()):
    print("Reloading data...")
    direc="~/simulations/ssd/200km_lagrangian6/"
    direc2="~/simulations/ssd/200km_eulerian3/"
    cfg=gemini3d.read.config(direc)
    xg=gemini3d.read.grid(direc)
    x=xg["x2"][2:-2]
    y=xg["x3"][2:-2]
    z=xg["x1"][2:-2]
    xg2=gemini3d.read.grid(direc2)
    x2=xg2["x2"][2:-2]
    y2=xg2["x3"][2:-2]
    z2=xg2["x1"][2:-2]
    it=5
    #dat=gemini3d.read.frame(direc,cfg["time"][it],var=parmlbl)
    #dat2=gemini3d.read.frame(direc2,cfg["time"][it],var=parmlbl)   
    dat=gemini3d.read.frame(direc,cfg["time"][it])
    dat2=gemini3d.read.frame(direc2,cfg["time"][it])   

# Compare the requested parameter
plt.subplots(len(altref),2,dpi=150)
for ialt in range(0,len(altref)):
    iz=np.argmin(abs(z-altref[ialt]))
    plt.subplot(len(altref),2,2*ialt+1)
    plt.pcolormesh(x,y,dat[parmlbl][iz,:,:])
    plt.colorbar()
    if (ialt==0):
        plt.title(str(cfg["time"][it]))
    iz2=np.argmin(abs(z2-altref[ialt]))
    plt.subplot(len(altref),2,2*ialt+2)
    plt.pcolormesh(x2,y2,dat2[parmlbl][iz2,:,:])
    plt.colorbar()
    if (ialt==0):
        plt.title(parmlbl)
    plt.show()


# Also compare potential solutions
if flagpot: 
    plt.subplots(1,2,dpi=150)
    plt.subplot(1,2,1)
    plt.pcolormesh(dat["Phitop"])
    plt.colorbar()
    plt.subplot(1,2,2)
    plt.pcolormesh(dat2["Phitop"])
    plt.colorbar()
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

