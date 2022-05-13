#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 08:55:20 2022

functions to do coordinate rotations

@author: zettergm
"""

from gemini3d.grid.convert import phin,thetan
from numpy import sin,cos,arccos,arctan2
import numpy as np

# Spherical to cartesian
def spherical2cart(r,theta,phi):
    z=r*cos(theta)
    x=r*sin(theta)*cos(phi)
    y=r*sin(theta)*sin(phi)
    return x,y,z

# Cartesian to spherical
def cart2spherical(x,y,z):
    r=np.sqrt(x**2+y**2+z**2)
    theta=arccos(z/r)
    phi=arctan2(y,x)
    return r,theta,phi

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

# Rotation matrix to go from geomagnetic to geographic
def Rgm2gg():
    return Rz(phin)@Ry(thetan)

# Transform ECEF geographic to ECEF geomagnetic
def rotgeog2geomag(xgg,ygg,zgg):
    r=np.array([xgg,ygg,zgg])
    return Rgg2gm()@r