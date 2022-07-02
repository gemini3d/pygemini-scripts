#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 09:18:28 2021

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
plotdir=direcs[0]+"/timeplots/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

# set env variables
os.environ["GEMINI_SIMROOT"]="~/simulations/"

# these are the same for each simulation
print("...Loading config and grid...")
cfg = gemini3d.read.config(direcs[0])
xg = gemini3d.read.grid(direcs[0])

# loop over simulations and times
Tivt=np.zeros( (lalt,len(cfg["time"]),ld) )
for j in range(0,ld):
    for i, simtime in enumerate(cfg["time"]):
        if j==0 and i>12:
            continue
        else:
            print("  Loading:  "+direcs[j]+str(cfg["time"][i]))
            dat=gemini3d.read.frame(direcs[j],simtime)
            alti, mloni, mlati, parami = model2magcoords(xg, dat["Ti"], lalt, llon, llat)
            ilon=llon//2
            ilat=llat//2
            Tivt[:,i,j]=parami[:,ilon,ilat]

# make a plot v time
plt.subplots(ld,1,dpi=150,figsize=(8.5,8.5) )
for j in range(0,ld):
    plt.subplot(ld,1,j+1)
    plt.pcolor(cfg["time"],alti/1e3,Tivt[:,:,j])
    plt.xlabel("UT")
    plt.ylabel("altitude (km)")
    plt.ylim(90,500)
    if j==0:
        plt.title("$T_i$ (K)")
    plt.colorbar()

plt.show(block=False)
plt.savefig(plotdir+"/timeseries.png")

