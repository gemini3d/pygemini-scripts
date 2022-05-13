#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 20:39:11 2022

@author: zettergm
"""

import numpy as np
from gemini3d.grid.convert import Re,geog2geomag
from numpy import pi
from rotfns import Rgg2gm,Rgm2gg,spherical2cart,cart2spherical,rotgeog2geomag

##############################################################################
glat=45
glon=45
thetag=pi/2-glat*pi/180
phig=glon*pi/180
rg=Re

# ECEF geographic to geomagnetic conversion
[xgg,ygg,zgg]=spherical2cart(rg,thetag,phig)
rgg=np.array([xgg,ygg,zgg])
[xgm,ygm,zgm]=rotgeog2geomag(xgg,ygg,zgg)
rgm=np.array([xgm,ygm,zgm])

# Check that transformation is unitary
rgg2=Rgg2gm().transpose()@rgm
print("\n Test fwd/inv transformation:  ",rgg,rgg2)
print("\n Test unitary:  ")
print(Rgm2gg()@Rgg2gm())
print(Rgg2gm()@Rgm2gg())

# store out rotation matrix
rotmat=Rgg2gm()

# compute spherical magentic, i.e. magnetic latitude and longitude
rgmspher=cart2spherical(xgm,ygm,zgm)
mlat=90-rgmspher[1]*180/pi
mlon=rgmspher[2]*180/pi

# Check spherical magnetic from existing transformations in pygemini
[phim,thetam]=geog2geomag(glon,glat)
mlat2=90-thetam*180/pi
mlon2=phim*180/pi

print("\n Mag. coords comparison:  ",mlon,mlon2,mlat,mlat2)
##############################################################################

