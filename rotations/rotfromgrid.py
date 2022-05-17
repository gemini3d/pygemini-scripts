#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 09:04:24 2022

@author: zettergm
"""

import gemini3d.read
from rotfns import Rgm2gg
import numpy as np
from numpy import pi,sin,cos
import matplotlib.pyplot as plt

print("Reading data...")
direc="~/simulations/raid/aurora_EISCAT3D_simple_wide/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,time=cfg["time"][-1])

lx1=xg["lx"][0]; lx2=xg["lx"][1]; lx3=xg["lx"][2];

# convert vectors in model basis to geomagnetic ECEF comps. using stored unit vectors
print("Rotate internal coords to geomag. spherical...")
vrgm=( np.sum(xg["e1"]*xg["er"],3)*dat["v1"] + np.sum(xg["e2"]*xg["er"],3)*dat["v2"] + 
    np.sum(xg["e3"]*xg["er"],3)*dat["v3"] )
vthetagm=( np.sum(xg["e1"]*xg["etheta"],3)*dat["v1"] + np.sum(xg["e2"]*xg["etheta"],3)*dat["v2"] +
    np.sum(xg["e3"]*xg["etheta"],3)*dat["v3"] )
vphigm=( np.sum(xg["e1"]*xg["ephi"],3)*dat["v1"] + np.sum(xg["e2"]*xg["ephi"],3)*dat["v2"] + 
    np.sum(xg["e3"]*xg["ephi"],3)*dat["v3"] )

# At this point the components are in geomagnetic spherical
print("Convert geomagnetic spherical to geomagnetic ECEF (Cartesian)")
vxgm=vrgm*xg["er"][:,:,:,0]+vthetagm*xg["etheta"][:,:,:,0]+vphigm*xg["ephi"][:,:,:,0]
vygm=vrgm*xg["er"][:,:,:,1]+vthetagm*xg["etheta"][:,:,:,1]+vphigm*xg["ephi"][:,:,:,1]
vzgm=vrgm*xg["er"][:,:,:,2]+vthetagm*xg["etheta"][:,:,:,2]+vphigm*xg["ephi"][:,:,:,2]

# now rotation geomagnetic ECEF into geographic ECEF one grid location at a time
print("Rotate geomag ECEF to geographic ECEF...")
vxgmflat=np.reshape(np.array(vxgm),[1,lx1*lx2*lx3],order='F')
vygmflat=np.reshape(np.array(vygm),[1,lx1*lx2*lx3],order='F')
vzgmflat=np.reshape(np.array(vzgm),[1,lx1*lx2*lx3],order='F')
vgm=np.concatenate((vxgmflat,vygmflat,vzgmflat), axis=0)
vgg=Rgm2gg()@vgm
vxgg=np.reshape(vgg[0,:],[lx1,lx2,lx3],order='F')
vygg=np.reshape(vgg[1,:],[lx1,lx2,lx3],order='F')
vzgg=np.reshape(vgg[2,:],[lx1,lx2,lx3],order='F')

# finally we want to convert to geographic spherical
print("Convert geographic ECEF to geographic spherical")
thetagg=pi/2-xg["glat"]*pi/180
phigg=xg["glon"]*pi/180
vrgg=sin(thetagg)*cos(phigg)*vxgg+sin(thetagg)*sin(phigg)*vygg+cos(thetagg)*vzgg
vthetagg=cos(thetagg)*cos(phigg)*vxgg+cos(thetagg)*sin(phigg)*vygg-sin(thetagg)*vzgg
vphigg=-sin(phigg)*vxgg+cos(phigg)*vygg

# check magnitudes
vmaggg=np.sqrt(vrgg**2+vthetagg**2+vphigg**2)
vmaggm=np.sqrt(vrgm**2+vthetagm**2+vphigm**2)
print("Magnitude comparison test:  ",vmaggm-vmaggg)

# plot a "center cut"
plt.subplots(3,3)

plt.subplot(3,3,2)
plt.pcolormesh(vrgm[:,:,64])
plt.colorbar()

plt.subplot(3,3,3)
plt.pcolormesh(vrgg[:,:,64])
plt.colorbar()

plt.subplot(3,3,5)
plt.pcolormesh(vthetagm[:,:,64])
plt.colorbar()

plt.subplot(3,3,6)
plt.pcolormesh(vthetagg[:,:,64])
plt.colorbar()

plt.subplot(3,3,8)
plt.pcolormesh(vphigm[:,:,64])
plt.colorbar()

plt.subplot(3,3,9)
plt.pcolormesh(vphigg[:,:,64])
plt.colorbar()

plt.subplot(3,3,1)
plt.pcolormesh(dat["v1"][:,:,64])
plt.colorbar()

plt.subplot(3,3,4)
plt.pcolormesh(dat["v2"][:,:,64])
plt.colorbar()

plt.subplot(3,3,7)
plt.pcolormesh(dat["v3"][:,:,64])
plt.colorbar()

#  This is amazingly slow...
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

