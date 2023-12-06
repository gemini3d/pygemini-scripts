#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:16:45 2023

@author: zettergm
"""

#!/usr/bin/env python3
"""
@author: zettergm
"""


def padstr(simtime,simtimestr):
    simtimestrout=simtimestr
    if simtime<10:
        simtimestrout="0000"+simtimestrout
    elif simtime<100:
        simtimestrout="000"+simtimestrout
    elif simtime<1000:
        simtimestrout="00"+simtimestrout
    elif simtime<10000:
        simtimestrout="0"+simtimestrout
    return simtimestrout


import gemini3d.read
#from plotcurv import plotcurv2D
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2geogcoords
import numpy as np
import os

parmlbl="ne"

# load some sample data (2D)
direc = "/Users/zettergm/simulations/raid2/simulations_eclipse/Oct2023_eclipse_solmax_20_3Dv2/"
cfg = gemini3d.read.config(direc)
xg = gemini3d.read.grid(direc)

# info needed to write output plots
plotdir=direc+"/plots_sampled/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

# make plots for each time
plt.ioff()    # so matplotlib doesn't take over the entire computer :(
plt.figure(1,dpi=150)
plt.figure(2,dpi=150)
for it in range(0,len(cfg["time"])):
    print("Sampling model results in geographic coords for time step:  ",cfg["time"][it])
    dat = gemini3d.read.frame(direc, cfg["time"][it], var=parmlbl)   
    
    # grid data
    lalt = 384
    llat = 384
    llon = 128
    altlims=(0,750e3)
    lonlims=(np.min(xg["glon"]),np.max(xg["glon"]))
    latlims=(np.min(xg["glat"]),np.max(xg["glat"]))
    parm = dat[parmlbl]
    alti, gloni, glati, parmgeoi = model2geogcoords(xg, parm, lalt, llon, llat, altlims, lonlims, latlims)
    parmgeoi=parmgeoi.reshape((lalt,llon,llat))
    
    # now plot interpolated data
    ecglon=360-106;
    ilon=np.argmin(abs(gloni-ecglon))
    plt.figure(1)
    plt.clf()
    plt.axes().set_aspect(1/16)   
    plt.pcolormesh(glati,alti/1e3,parmgeoi[:,ilon,:],shading="interp")
    plt.ylim((0,750))
    plt.colorbar(label="$n_e$ ")
    plt.ylabel("altitude (km)")
    plt.xlabel("geog. lat.")
    
    simtime=(cfg["time"][it]-cfg["time"][0]).total_seconds()+7200
    plt.title("$\Delta n_e$ @ 300 km altitude (pct.):  "+str(simtime/60)+" min.")
    simtimestr=str(simtime)
    simtimestr=padstr(simtime,simtimestr)
    plt.savefig(plotdir+"/"+parmlbl+"_altlat_"+simtimestr+"s.png")
    
    altref=325e3
    plt.figure(2)
    plt.clf()
    ialt=np.argmin(abs(alti-altref))
    plt.pcolormesh(gloni,glati,parmgeoi[ialt,:,:].transpose(),shading="interp")
    plt.colorbar(label="$n_e$ ")
    plt.ylabel("geog. lat.")
    plt.xlabel("geog. lon.")
    plt.savefig(plotdir+"/"+parmlbl+"_lonlat_"+simtimestr+"s.png")
    
    # # extract a meaningful profile for the experiment
    # ecglat=33.0
    # ilat=np.argmin(abs(glati-ecglat))
    # plt.figure(dpi=150)
    # plt.plot(np.log10(parmgeoi[:,ilon,ilat]),alti/1e3)
    # plt.xlim((9, 12.7))
    # plt.ylim((0, 750))
    # plt.xlabel("log$_{10}$ plasma density")
    # plt.ylabel("altitude")
