#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 19:30:09 2021

@author: zettergm
"""

# imports
import gemini3d.read
import numpy as np
import matplotlib.pyplot as plt
import os
from gemini3d.grid.gridmodeldata import model2magcoords

# number of interpolation sites
lalt=512
llon=32
llat=512

# location of simulation output
direcs = (["/Users/zettergm/simulations/said_curv_long_J0.85_Q0.02",
          "/Users/zettergm/simulations/said_curv_long_J0.85_Q0.04",
          "/Users/zettergm/simulations/said_curv_long_J0.85_Q0.06"])
ld=len(direcs)

# make a directory in which to store line plots
plotdir=direcs[0]+"/satplots/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

# set env variables
os.environ["GEMINI_SIMROOT"]="~/simulations/"

# these are the same for each simulation
print("...Loading config and grid...")
cfg = gemini3d.read.config(direcs[0])
xg = gemini3d.read.grid(direcs[0])

# parameters to plot
params=["ne","Ti","Te","v3"]
paramslbl=["$n_e$ (m$^{-3})$","$T_i$ (K)","$T_e (K)$","$v_E$ (m/s)"]
lp=len(params)
dati=np.zeros( (lp,len(direcs),lalt,llon,llat) )

# loop over simulations and times
for simtime in cfg["time"]:
    plt.subplots(4,1,dpi=100,figsize=(8.5,8.5) )
    timelbl=str(simtime)
    
    for i, direc in enumerate(direcs):
        print("  Loading:  "+timelbl)
        dat=gemini3d.read.frame(direc,simtime)
        for j, param in enumerate(params):
            alti, mloni, mlati, parami = model2magcoords(xg, dat[param], lalt, llon, llat)     # grid the data
            dati[j,i,:,:,:]=parami
            ialt=np.argmin(np.abs(alti-500e3))
            ilon=llon//2
            plt.subplot(lp,1,j+1)
            plt.plot(mlati,parami[ialt,ilon,:])
            plt.xlabel("mag. lat. (deg.)")
            plt.ylabel(paramslbl[j])
            if j==0:
                plt.title(timelbl)
            
    plt.legend(("Q=0.02 mW/m$^2$","Q=0.04 mW/m$^2$","Q=0.06 mW/m$^2$"))
    plt.savefig(plotdir+"/"+timelbl+".png")
    plt.close("all")
