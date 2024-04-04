#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:26:43 2024

@author: zettergm
"""

import gemini3d.read
import gemini3d.magtools
import gemini3d.coord
import numpy as np
import matplotlib.pyplot as plt

mu0=4*np.pi*1e-7

direc="/Users/zettergm/simulations/sdcard/aurora_null_02/"
fname="20150201_35880.000000.h5"
#direc="/Users/zettergm/simulations/sdcard/arcs/"
#fname="20170302_27060.000000.h5"

cfg=gemini3d.read.config(direc)
#xg=gemini3d.read.grid(direc)
magdir=direc+"magfields/"
magdat=gemini3d.magtools.magframe(magdir+fname)

Hx=magdat["Bphi"]/mu0
Hx=Hx[0,:,:]
Hy=-1*magdat["Btheta"]/mu0
Hy=Hy[0,:,:]
mlon=magdat["mlon"]
mlat=magdat["mlat"]
alt=magdat["r"]-6370e3

theta=np.deg2rad(90-mlat)
idx=np.argsort(theta)    # theta runs opposite of mlat,x -- so we need to sort the mag field arrays
phi=np.deg2rad(mlon)
Hx=Hx[:,idx]
Hy=Hy[:,idx]
ALT,THETA,PHI = np.meshgrid(alt,theta,phi,indexing="ij")
GLAT,GLON = gemini3d.coord.geomag2geog(THETA, PHI)
Z,X,Y = gemini3d.coord.geog2UEN(ALT, GLON, GLAT, theta.mean(), phi.mean())
x=X[0,0,:]
y=Y[0,:,0]

Hyx,_=np.gradient(Hy,x,y)
_,Hxy=np.gradient(Hx,x,y)
Jz=Hyx-Hxy


###############################################################################
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc+fname)
J1=dat["J1"]
x2=xg["x2"][2:-2]
x3=xg["x3"][2:-2]

plt.subplots(2,1,dpi=100)
plt.subplot(2,1,1)
plt.pcolormesh(x2,x3,J1[-1,:,:].transpose())
plt.colorbar()
plt.xlabel("x")
plt.ylabel("y")
xlims=plt.xlim()
ylims=plt.ylim()
plt.title("$J_1$")

plt.subplot(2,1,2)
plt.pcolormesh(x,y,Jz.transpose())
plt.colorbar()
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(xlims)
plt.ylim(ylims)
plt.title("$\partial_x H_y - \partial_y H_x$")

###############################################################################
plt.subplots(2,1,dpi=100)
plt.subplot(2,1,1)
plt.pcolormesh(x,y,Hx.transpose())
plt.colorbar()
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(xlims)
plt.ylim(ylims)
plt.title("$H_x$")

plt.subplot(2,1,2)
plt.pcolormesh(x,y,Hy.transpose())
plt.colorbar()
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(xlims)
plt.ylim(ylims)
plt.title("$H_y$")
###############################################################################


