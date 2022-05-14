#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 09:04:24 2022

@author: zettergm
"""

import gemini3d.read
from rotfns import rotgeomag2geog,Rgm2gg
import numpy as np

direc="~/simulations/raid/aurora_EISCAT3D_simple_wide/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,time=cfg["time"][-1])

lx1=xg["lx"][0]; lx2=xg["lx"][1]; lx3=xg["lx"][2];

# convert vectors in model basis to geomagnetic ECEF comps. using stored unit vectors
vrgm=( np.sum(xg["e1"]*xg["er"],3)*dat["v1"] + np.sum(xg["e2"]*xg["er"],3)*dat["v2"] + 
    np.sum(xg["e3"]*xg["er"],3)*dat["v3"] )
vthetagm=( np.sum(xg["e1"]*xg["etheta"],3)*dat["v1"] + np.sum(xg["e2"]*xg["etheta"],3)*dat["v2"] +
    np.sum(xg["e3"]*xg["etheta"],3)*dat["v3"] )
vphigm=( np.sum(xg["e1"]*xg["ephi"],3)*dat["v1"] + np.sum(xg["e2"]*xg["ephi"],3)*dat["v2"] + 
    np.sum(xg["e3"]*xg["ephi"],3)*dat["v3"] )

# now rotation geomagnetic ECEF into geographic ECEF one grid location at a time
print("Staring rotations...")
vrgm=np.reshape(np.array(vrgm),[1,lx1*lx2*lx3],order='F')
vthetagm=np.reshape(np.array(vthetagm),[1,lx1*lx2*lx3],order='F')
vphigm=np.reshape(np.array(vphigm),[1,lx1*lx2*lx3],order='F')
vgm=np.concatenate((vrgm,vthetagm,vphigm), axis=0)
vgg=Rgm2gg()@vgm
vrgg=np.reshape(vgg[0,:],[lx1,lx2,lx3],order='F')
vthetagg=np.reshape(vgg[1,:],[lx1,lx2,lx3],order='F')
vphigg=np.reshape(vgg[2,:],[lx1,lx2,lx3],order='F')



# vrgg=np.zeros( (lx1,lx2,lx3) )
# vthetagg=np.zeros( (lx1,lx2,lx3) )
# vphigg=np.zeros( (lx1,lx2,lx3) )
# for i1 in range(0,lx1):
#     for i2 in range(0,lx2):
#         for i3 in range(0,lx3):
#             vgg=rotgeomag2geog(vrgm[i1,i2,i3],vthetagm[i1,i2,i3],vphigm[i1,i2,i3])
#             vrgg[i1,i2,i3]=vgg[0]
#             vthetagg[i1,i2,i3]=vgg[1]
#             vphigg[i1,i2,i3]=vgg[2]

