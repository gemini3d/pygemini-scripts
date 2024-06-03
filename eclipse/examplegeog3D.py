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


import gemini3d.read
#from plotcurv import plotcurv2D
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2geogcoords
import numpy as np
import os
import utilstr

parmlbl=["ne","v1","Te","Ti"]

# load some sample data (2D)
direc = "/Users/zettergm/simulations/ssd/Oct2023_annular_eclipse_datamask4/"
#direc = "/Users/zettergm/simulations/ssd/Apr2024_total_eclipse_datamask3/"
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
        
        # now plot interpolated data
        ecglon=360-106;
        ilon=np.argmin(abs(gloni-ecglon))
        plt.figure(1)
        plt.clf()
        plt.axes().set_aspect(1/16)   
        plt.pcolormesh(glati,alti/1e3,parmgeoi[:,ilon,:],shading="interp")
        plt.ylim((0,750))
        plt.colorbar(label=parmlbl[ilbl])
        plt.ylabel("altitude (km)")
        plt.xlabel("geog. lat.")
        
        simtime=(cfg["time"][it]-cfg["time"][0]).total_seconds()+7200
        plt.title(parmlbl[ilbl]+" @"+str(gloni[ilon])+" deg. glon. "+str(cfg["time"][it]))
        simtimestr=str(simtime)
        simtimestr=utilstr.padstr(simtime,simtimestr)
        plt.savefig(plotdir+"/"+parmlbl[ilbl]+"_altlat_"+simtimestr+"s.png")
        
        altref=250e3
        plt.figure(2)
        plt.clf()
        ialt=np.argmin(abs(alti-altref))
        plt.pcolormesh(gloni,glati,parmgeoi[ialt,:,:].transpose(),shading="interp")
        plt.colorbar(label=parmlbl[ilbl])
        plt.ylabel("geog. lat.")
        plt.xlabel("geog. lon.")
        plt.title(parmlbl[ilbl]+" @ "+str(altref/1e3)+" km altitude:  "+str(cfg["time"][it]))
        plt.savefig(plotdir+"/"+parmlbl[ilbl]+"_lonlat_"+simtimestr+"s.png")
        
        # # extract a meaningful profile for the experiment
        # ecglat=33.0
        # ilat=np.argmin(abs(glati-ecglat))
        # plt.figure(dpi=150)
        # plt.plot(np.log10(parmgeoi[:,ilon,ilat]),alti/1e3)
        # plt.xlim((9, 12.7))
        # plt.ylim((0, 750))
        # plt.xlabel("log$_{10}$ plasma density")
        # plt.ylabel("altitude")
