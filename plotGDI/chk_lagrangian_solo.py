#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:27:14 2023

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
import numpy as np

flagpot=False

parmlbl="J3"
altref=[90e3,115e3,300e3,600e3,800e3]

if not ("xg" in locals()):
    print("Reloading data...")
    direc="~/simulations/ssd/200km_lagrangian_lowres/"
    cfg=gemini3d.read.config(direc)
    xg=gemini3d.read.grid(direc)
    x=xg["x2"][2:-2]
    y=xg["x3"][2:-2]
    z=xg["x1"][2:-2]
    it=20
    #dat=gemini3d.read.frame(direc,cfg["time"][it],var=parmlbl)
    #dat2=gemini3d.read.frame(direc2,cfg["time"][it],var=parmlbl)   
    dat=gemini3d.read.frame(direc,cfg["time"][it])

# Compare the requested parameter
plt.subplots(len(altref),1,dpi=150)
for ialt in range(0,len(altref)):
    iz=np.argmin(abs(z-altref[ialt]))
    plt.subplot(len(altref),2,ialt+1)
    plt.pcolormesh(x,y,dat[parmlbl][iz,:,:].transpose())
    plt.colorbar()
    if (ialt==0):
        plt.title(str(cfg["time"][it]))
    plt.show()


# Also compare potential solutions
if flagpot: 
    plt.subplots(1,2,dpi=150)
    plt.subplot(1,2,1)
    plt.pcolormesh(dat["Phitop"])
    plt.colorbar()
    plt.show()
