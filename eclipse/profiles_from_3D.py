#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 16:18:48 2023

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2geogcoords
import numpy as np
import os
import datetime
import path

# Reference location
#refglat=33.2
#refglon=253.66
refglat=44.5
refglon=360-73.2

# load some sample data (2D)
direc = "/Users/zettergm/simulations/ssd/eclipse/Oct2023_annular_eclipse_datamask4/"
cfg = gemini3d.read.config(direc)
xg = gemini3d.read.grid(direc)
lx1=xg["lx"][0]
lx2=xg["lx"][1]
lx3=xg["lx"][2]
lt=len(cfg["time"])

# info needed to write output plots
plotdir=direc+"/plots_sampled/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)


# target grid for sampling
lalt = 512
llat = 384
llon = 256
altlims=(0,750e3)
lonlims=(np.min(xg["glon"]),np.max(xg["glon"]))
latlims=(np.min(xg["glat"]),np.max(xg["glat"]))


# Extract referece time index
UTsecref=int(np.round(path.getreftime(refglon,refglat)))
UThr=UTsecref//3600
UTmin=(UTsecref-3600*UThr)//60
UTsec=(UTsecref-3600*UThr-60*UTmin)
UTref=datetime.datetime(cfg["time"][-1].year, cfg["time"][-1].month, cfg["time"][-1].day, UThr, UTmin, UTsec)

dtmin=np.Infinity
itref=-1
for it in range(0,lt):
    now=cfg["time"][it]
    dt=(now-UTref).total_seconds()
    if abs(dt)<dtmin:
        itref=it
        dtmin=abs(dt)


# Extract time indices for various instances near annularity
dtshift=30*60
dtout=int(cfg["dtout"].total_seconds())
indshift=dtshift//dtout
#itlist=[itref-2*indshift,itref-indshift,itref,itref+indshift,itref+2*indshift]
itlist=[itref-indshift,itref,itref+indshift]

# load the times of interest into workspace
ne=np.empty((lalt,llon,llat,len(itlist)))
Te=np.empty((lalt,llon,llat,len(itlist)))
for indind in range(0,len(itlist)):
    print("Sampling model results in geographic coords for time step:  ",cfg["time"][itlist[indind]])
    dat = gemini3d.read.frame(direc, cfg["time"][itlist[indind]])  
    
    alti, gloni, glati, negeoi = model2geogcoords(xg, dat["ne"], lalt, llon, llat, altlims, lonlims, latlims)
    negeoi=negeoi.reshape((lalt,llon,llat))    
#    alti, gloni, glati, Tegeoi = model2geogcoords(xg, dat["Te"], lalt, llon, llat, altlims, lonlims, latlims)
#    Tegeoi=Tegeoi.reshape((lalt,llon,llat))   
    alti, gloni, glati, Tegeoi = model2geogcoords(xg, dat["Ti"], lalt, llon, llat, altlims, lonlims, latlims)
    Tegeoi=Tegeoi.reshape((lalt,llon,llat))   
    ne[:,:,:,indind]=negeoi
    Te[:,:,:,indind]=Tegeoi
    
    
# Extract reference lat/lon
ilatref=np.argmin(abs( glati - refglat ))
ilonref=np.argmin(abs( gloni - refglon ))
    

# Print the figure
plt.subplots(1,2,dpi=150)
for indind in range(0,len(itlist)):
    neprof=ne[:,ilonref,ilatref,indind]
    Teprof=Te[:,ilonref,ilatref,indind]
    
    plt.subplot(1,2,1)
    plt.semilogx(neprof,alti/1e3)
    plt.ylim((90,350))
    plt.xlim((1e10,2e12))
    plt.xlabel("$n_e$ (m$^{-3}$)")
    plt.ylabel("altitude (km)")
    
    plt.subplot(1,2,2)
    plt.plot(Teprof,alti/1e3)
    plt.xlim((0,2000))
    plt.ylim((90,350))
    plt.xlabel("$T_i$ (K)")
    #plt.ylabel("altitude (km)")
    
#plt.legend(["$t_0$ - 60 min.","$t_0$ - 30 min.","$t_0$","$t_0$ + 30 min.","$t_0$ + 60 min."])
plt.legend(["$t_0$ - 30 min.","$t_0$","$t_0$ + 30 min."])


# Save to a file
plotdir=direc+"/plots_profiles/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)
plt.savefig(plotdir+"/profiles.png")
    