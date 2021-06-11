#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zettergm
"""

# imports
from gemini3d.grid.gridmodeldata import model2magcoords
import matplotlib.pyplot as plt
import numpy as np


# plot dipole data vs. alt,lon,lat
def plotcurv3D(xg,parm,cfg,lalt=256,llon=256,llat=256):
    # grid data; wasteful and should only do a slice at a time???
    [alti,mloni,mlati,parmi]=model2magcoords(xg,parm,lalt,llon,llat)
    
    # define slices indices
    altref=300e3
    ialt=np.argmin(abs(alti-altref))
    lonavg=cfg["sourcemlon"]
    ilon=np.argmin(abs(mloni-lonavg))
    latavg=cfg["sourcemlat"]
    ilat=np.argmin(abs(mlati-latavg))
    
    # plot various slices through the 3D domain
    plt.subplots(1,3)
    
    plt.subplot(1,3,1)
    plt.pcolormesh(mloni,alti/1e3,parmi[:,:,ilat])
    plt.xlabel('mlon')
    plt.ylabel('alt')
    plt.colorbar()
    
    plt.subplot(1,3,2)
    plt.pcolormesh(mloni,mlati,parmi[ialt,:,:].transpose())
    plt.xlabel('mlon')
    plt.ylabel('mlat')
    plt.colorbar()
    
    plt.subplot(1,3,3)
    plt.pcolormesh(mlati,alti/1e3,parmi[:,ilon,:])
    plt.xlabel('mlat')
    plt.ylabel('alt')
    plt.colorbar()
    plt.show(block=False)

    return


# alt,lon plot for 2D dipole data
def plotcurv2D(xg,parm,lalt=512,llat=512):
    # grid data
    [alti,mloni,mlati,parmi]=model2magcoords(xg,parm,lalt,1,llat)
    
    # define slices indices, for 2D there is only one longitude index
    ilon=0
    
    # plot the meridional slice
    plt.figure()
    plt.pcolormesh(mlati,alti/1e3,parmi[:,ilon,:])
    plt.xlabel('mlat')
    plt.ylabel('alt')
    plt.colorbar()
    plt.show(block=False)

    return
