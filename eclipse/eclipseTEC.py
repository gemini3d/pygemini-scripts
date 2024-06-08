#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: zettergm
"""


import gemini3d.read
#from plotcurv import plotcurv2D
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2geogcoords
import numpy as np
import os
import utilstr

parmlbl=["ne"]

# load some sample data (2D)
#direc = "/Users/zettergm/simulations/ssd/eclipse/Oct2023_annular_eclipse_datamask4/"
direc = "/Users/zettergm/simulations/ssd/eclipse/Apr2024_total_eclipse_datamask3/"
cfg = gemini3d.read.config(direc)
xg = gemini3d.read.grid(direc)

# info needed to write output plots
plotdir=direc+"/plots_sampled/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

# make plots for each time
plt.ioff()    # so matplotlib doesn't take over the entire computer :(
plt.figure(1,dpi=150)
for ilbl in range(0,len(parmlbl)):
    for it in range(0,len(cfg["time"])):
        print("Sampling model results in geographic coords for time step:  ",cfg["time"][it]," paramter:  ",parmlbl[ilbl])
        dat = gemini3d.read.frame(direc, cfg["time"][it], var=parmlbl[ilbl])   
        
        # grid data
        lalt = 384
        llat = 384
        llon = 256
        altlims=(0,750e3)
        lonlims=(np.min(xg["glon"]),np.max(xg["glon"]))
        latlims=(np.min(xg["glat"]),np.max(xg["glat"]))
        parm = dat[parmlbl[ilbl]]
        alti, gloni, glati, parmgeoi = model2geogcoords(xg, parm, lalt, llon, llat, altlims, lonlims, latlims)
        parmgeoi=parmgeoi.reshape((lalt,llon,llat))
        parmgeoi[np.isnan(parmgeoi)]=0.0
        
        # compute total electron content
        TEC=np.trapz(parmgeoi,alti,axis=0)
        TEC=TEC/1e16
        TEC[TEC<0.1]=np.NaN
        
        # set up time labels
        simtime=(cfg["time"][it]-cfg["time"][0]).total_seconds()+7200
        simtimestr=str(simtime)
        simtimestr=utilstr.padstr(simtime,simtimestr)
        plt.savefig(plotdir+"/"+parmlbl[ilbl]+"_altlat_"+simtimestr+"s.png")
        
        altref=250e3
        plt.figure(2)
        plt.clf()
        ialt=np.argmin(abs(alti-altref))
        plt.pcolormesh(gloni,glati,TEC.transpose(),shading="interp")
        plt.colorbar(label="TEC")
        plt.ylabel("geog. lat.")
        plt.xlabel("geog. lon.")
        plt.title("TEC"+" "+str(cfg["time"][it]))
        plt.savefig(plotdir+"/"+"TEC"+"_lonlat_"+simtimestr+"s.png")

