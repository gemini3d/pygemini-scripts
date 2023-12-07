#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:34:15 2023

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
import numpy as np

parmlbl="J3"

direc="~/simulations/raid2/simulations_MR/200km_lagrangian6/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
x=xg["x2"][2:-2]
y=xg["x3"][2:-2]
z=xg["x1"][2:-2]
lx1=xg["lx"][0]
lx2=xg["lx"][1]
lx3=xg["lx"][2]

lt=len(cfg["time"])
parm=np.empty((lx1,lx2,lx3,lt))
for it in range(0,lt):
    print(cfg["time"][it])
    dat=gemini3d.read.frame(direc,cfg["time"][it],var=parmlbl)
    parm[:,:,:,it]=dat[parmlbl]
    
# plt.figure()
# altref=300e3
# ialt=np.argmin(abs(z-altref))
# dataplot=parm[ialt,]