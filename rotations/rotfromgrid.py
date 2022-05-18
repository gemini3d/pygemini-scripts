#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 09:04:24 2022

@author: zettergm
"""

import gemini3d.read
from rotfns import Rgm2gg,Rgg2gm
import numpy as np
from numpy import pi,sin,cos
import matplotlib.pyplot as plt

##############################################################################
# defs
##############################################################################
def rotvec_gg2gm(e):
    [lx1,lx2,lx3,lcomp]=e.shape
    ex=np.array(e[:,:,:,0])
    ey=np.array(e[:,:,:,1])
    ez=np.array(e[:,:,:,2])
    exflat=np.reshape(ex,[1,lx1*lx2*lx3],order="F")
    eyflat=np.reshape(ey,[1,lx1*lx2*lx3],order="F")
    ezflat=np.reshape(ez,[1,lx1*lx2*lx3],order="F")
    emat=np.concatenate((exflat,eyflat,ezflat), axis=0)
    egg=Rgg2gm()@emat
    eggshp=np.zeros((lx1,lx2,lx3,3))
    eggshp[:,:,:,0]=np.reshape(egg[0,:],[lx1,lx2,lx3],order="F")
    eggshp[:,:,:,1]=np.reshape(egg[1,:],[lx1,lx2,lx3],order="F")
    eggshp[:,:,:,2]=np.reshape(egg[2,:],[lx1,lx2,lx3],order="F")    
    return eggshp
#############################################################################


print("Reading data...")
direc="~/simulations/aurora_EISCAT3D_simple_wide/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,time=cfg["time"][-1])

lx1=xg["lx"][0]; lx2=xg["lx"][1]; lx3=xg["lx"][2];

##############################################################################
# the long way
##############################################################################

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
##############################################################################

##############################################################################
# Could also precompute projections like in fortran code by computing geographic unit vectors
#   in geomagnetic ECEF components.  This can be done by:
#   spherical gm comps -> ECEF gm comps -> ECEF gg comps -> spherical gg comps
#   For this case the final results will be gg unit vecs but in gm ECEF comps.
#   Or we can just generate the geographic unit vectors and rotate those into
#   a the ECEF geomag system.  
##############################################################################
thetagg=pi/2-xg["glat"]*pi/180
phigg=xg["glon"]*pi/180

ergg=np.empty((lx1,lx2,lx3,3))
ethetagg=np.empty((lx1,lx2,lx3,3))
ephigg=np.empty((lx1,lx2,lx3,3))
ergg[:,:,:,0]=sin(thetagg)*cos(phigg)
ergg[:,:,:,1]=sin(thetagg)*sin(phigg)
ergg[:,:,:,2]=cos(thetagg)
ethetagg[:,:,:,0]=cos(thetagg)*cos(phigg)
ethetagg[:,:,:,1]=cos(thetagg)*sin(phigg)
ethetagg[:,:,:,2]=-sin(thetagg)
ephigg[:,:,:,0]=-sin(phigg)
ephigg[:,:,:,1]=cos(phigg)
ephigg[:,:,:,2]=np.zeros(thetagg.shape)

ergg2gm=rotvec_gg2gm(ergg)
ethetagg2gm=rotvec_gg2gm(ethetagg)
ephigg2gm=rotvec_gg2gm(ephigg)

print("Rotate internal coords to geographic spherical directly using geograhpic unit vecs...")
vrgg2=( np.sum(xg["e1"]*ergg2gm,3)*dat["v1"] + np.sum(xg["e2"]*ergg2gm,3)*dat["v2"] + 
    np.sum(xg["e3"]*ergg2gm,3)*dat["v3"] )
vthetagg2=( np.sum(xg["e1"]*ethetagg2gm,3)*dat["v1"] + np.sum(xg["e2"]*ethetagg2gm,3)*dat["v2"] +
    np.sum(xg["e3"]*ethetagg2gm,3)*dat["v3"] )
vphigg2=( np.sum(xg["e1"]*ephigg2gm,3)*dat["v1"] + np.sum(xg["e2"]*ephigg2gm,3)*dat["v2"] + 
    np.sum(xg["e3"]*ephigg2gm,3)*dat["v3"] )

plt.subplots(3,1)

plt.subplot(3,1,1)
plt.pcolormesh(vrgg2[:,:,64])
plt.colorbar()

plt.subplot(3,1,2)
plt.pcolormesh(vthetagg2[:,:,64])
plt.colorbar()

plt.subplot(3,1,3)
plt.pcolormesh(vphigg2[:,:,64])
plt.colorbar()
##############################################################################

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

