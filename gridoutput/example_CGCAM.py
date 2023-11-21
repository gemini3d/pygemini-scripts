#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 09:29:49 2023

@author: zettergm
"""

# imports
import gemini3d.read as read
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2geogcoords
import numpy as np
import os


def padstr(simtime,simtimestr):
    simtimestrout=simtimestr
    if simtime<1000:
        simtimestrout="0"+simtimestrout    
    if simtime<100:
        simtimestrout="0"+simtimestrout
    if simtime<10:
        simtimestrout="0"+simtimestrout
    return simtimestrout


# load some sample data (3D)
home=os.path.expanduser("~")
direc0= home+"/simulations/ssd/CGCAM_NZ_SHv2_control/"
direc = home+"/simulations/ssd/CGCAM_NZ_SHv2/"
cfg = read.config(direc)
lt=len(cfg["time"])
xg = read.grid(direc)
parmlbl="ne"

# produce gridding datasets from model
lalt=384; llon=384; llat=384;

# info needed to write output plots
plotdir=direc+"/plotsdiff/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

plt.figure(dpi=150)
for it in range(0,lt):
# regrid data in geographic
    print("Sampling model results in geographic coords for time step:  ",it)
    
    dat0 = read.frame(direc0, cfg["time"][it], var=parmlbl)
    dat = read.frame(direc, cfg["time"][it], var=parmlbl)    
    galti, gloni, glati, parmgi = model2geogcoords(xg, 
                                100*(dat[parmlbl]-dat0[parmlbl])/dat0[parmlbl],
                                lalt, llon, llat, wraplon=False)
    
    # make a plot
    # plt.figure(dpi=150)
    # dataplot=np.squeeze(parmgi[:,llon//2,:])
    # plt.pcolormesh(glati,galti,dataplot,shading="auto")
    # plt.colorbar()
    # plt.xlabel("latitude")
    # plt.ylabel("altitude")
    plt.clf()
    ialt=np.argmin(abs(galti-300e3))
    dataplot=np.squeeze(parmgi[ialt,:,:])
    plt.pcolormesh(gloni,glati,dataplot.transpose(),shading="auto")
    plt.colorbar()
    plt.ylabel("latitude")
    plt.xlabel("longitude")
    plt.title("percent variation in $n_e$ @ 300 km altitude")
    
    # plt.figure(dpi=150)
    # dataplot=np.squeeze(parmgi[:,:,llat//2])
    # plt.pcolormesh(gloni,galti,dataplot,shading="auto")
    # plt.colorbar()
    # plt.xlabel("longitude")
    # plt.ylabel("altitude")
    
    simtime=(cfg["time"][it]-cfg["time"][0]).total_seconds()
    simtimestr=str(simtime)
    simtimestr=padstr(simtime,simtimestr)
    plt.savefig(plotdir+"/"+parmlbl+simtimestr+"s_large.png")
        

