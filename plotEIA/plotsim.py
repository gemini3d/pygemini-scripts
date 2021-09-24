#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 20:33:43 2021

plot plasma density from fast simulations

@author: zettergm
"""
##############################################################################
# imports
import gemini3d.read
import os
import matplotlib.pyplot as plt
import numpy as np
from gemini3d.grid.gridmodeldata import model2magcoords

# functions    
def plotdata(z,y,parm,titlelbl,parmlbl):
    parmplot=np.squeeze(parm[:,0,:])
    
    plt.figure(num=0,dpi=300)
    plt.clf()
    plt.pcolormesh(y,z/1e3,np.log10(parmplot))
    plt.xlabel('mag. lat. (deg.)')
    plt.ylabel('altitude (km)')
    plt.ylim([90,1500])
    plt.colorbar(label="$log_{10} ~ n_e$")
    plt.clim([11,12.65])
    plt.title(titlelbl)
    ax=plt.gca()
    ax.set_aspect(1/40)
    #plt.show(block=False)
    return

##############################################################################
# prep
plt.close("all")

# setup output directories
direc="/Users/zettergm/simulations/raid/EIAwinds_reverse_large/"
plotdir=direc+"/customplots/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

# load config and grid
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
inds=np.arange(0,len(cfg["time"]))

# set resolution of plot grid
lalt = 1024
llat = 1024
llon = 1
parmlbl="ne"

# plots
for k in inds:
    print(cfg["time"][k])
    data=gemini3d.read.frame(direc,cfg["time"][k])                              # read the data
    parm=data[parmlbl]
    alti, mloni, mlati, parmi = model2magcoords(xg, parm, lalt, llon, llat)     # grid the data

    timelbl=str(cfg["time"][k])
    plotdata(alti,mlati,parmi,timelbl,parmlbl)
    simtime=(cfg["time"][k]-cfg["time"][0]).total_seconds()
    plt.savefig(plotdir+"/"+parmlbl+str(simtime)+"s.png")
    #wait=input("Press a button to continue...")
    
    
