#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 20:39:11 2022

@author: zettergm
"""

import gemini3d.grid.gridmodeldata
from gemini3d.grid.convert import Re,thetan,phin,geog2geomag
from numpy import sin,cos,pi,arccos,arctan2
import numpy as np


# Spherical to cartesian
def spherical2cart(r,theta,phi):
    z=r*cos(theta)
    x=r*sin(theta)*cos(phi)
    y=r*sin(theta)*sin(phi)
    return np.array([x,y,z])


# Cartesian to spherical
def cart2spherical(x,y,z):
    r=np.sqrt(x**2+y**2+z**2)
    theta=arccos(z/r)
    phi=arctan2(y,x)
    return np.array([r,theta,phi])


# Rotation about z axis with angle alpha
def Rz(alpha):
    R=np.zeros((3,3))
    R[0,0]=cos(alpha)
    R[0,1]=-sin(alpha)
    R[1,0]=sin(alpha)
    R[1,1]=cos(alpha)
    R[2,2]=1
    return R
    

# Rotation about y axis by angle alpha
def Ry(alpha):
    R=np.zeros((3,3))
    R[0,0]=cos(alpha)
    R[0,2]=sin(alpha)
    R[1,1]=1
    R[2,0]=-sin(alpha)
    R[2,2]=cos(alpha)
    return R

# Rotation matrix to go from geographic to geomagnetic coordinates; note the
#   rotation is done with angles -phin and -thetan so the transpose of the
#   standard rotation matrices are used
def Rgg2gm():    
    return (Ry(thetan)).transpose()@(Rz(phin)).transpose()


# Transform ECEF geographic to ECEF geomagnetic
def rotgeog2geomag(r):
    return Rgg2gm()@r


##############################################################################
glat=45
glon=45
thetag=pi/2-glat*pi/180
phig=glon*pi/180
rg=Re

[xgg,ygg,zgg]=spherical2cart(rg,thetag,phig)
rgg=np.array([xgg,ygg,zgg])
rgm=rotgeog2geomag(rgg)
xgm=rgm[0]; ygm=rgm[1]; zgm=rgm[2];

# Check that transformation is unitary
rgg2=Rgg2gm().transpose()@rgm
print(rgg,rgg2)

# Check out rotation matrix
rotmat=Rgg2gm()

# Check spherical magentic
rgmspher=cart2spherical(xgm,ygm,zgm)
mlat=90-rgmspher[1]*180/pi
mlon=rgmspher[2]*180/pi

# Check spherical magnetic from existing transformations
[phim,thetam]=geog2geomag(glon,glat)
mlat2=90-thetam*180/pi
mlon2=phim*180/pi

print(mlon,mlon2,mlat,mlat2)
##############################################################################
