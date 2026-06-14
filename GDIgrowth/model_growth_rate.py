#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 09:58:54 2026

Reads in simulation data and tries to compute an empirical growth rate

@author: zettergm
"""

import gemini3d.read
import numpy as np
import matplotlib.pyplot as plt

# Parameter to be analyzed
parmlbl="ne"

# User-specified values based on initial simulation frame inspection
x0=-655e3            # initial x-position of trailing edge of patch
z0=312e3             # hmF2

# Simulation information and grid
direc="~/simulations/sdcard/ONR_Lamarche/GDI_reference/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
Bmag=xg["Bmag"].mean()

# Cartesian coordinates (distance from RISR)
z=xg["x1"][2:-2]    # upward distance
x=xg["x2"][2:-2]    # northward distance
y=xg["x3"][2:-2]    # westward distance
lz=xg["lx"][0]      # number of cells in z-direction
lx=xg["lx"][1]
ly=xg["lx"][2]

# Organize timing info
lt=len(cfg["time"])      # number of simulation output files for this run
refdate=cfg["time"][0]

# geographic location of grid center
glat=xg["glat"].mean()
glon=xg["glon"].mean()

# read in the full time series, set drift, etc.
parm=np.empty((lz,lx,ly,lt))
tsec=np.empty((lt))
for it in range(0,lt):
    print(cfg["time"][it])
    dat=gemini3d.read.frame(direc,cfg["time"][it],var=parmlbl)
    parm[:,:,:,it]=dat[parmlbl]
    tsec[it]=(cfg["time"][it]-refdate).total_seconds()

    if (it==0):
        v = -cfg["Eyit"]/abs(Bmag)
        
# time series analysis for growth rate
iz=np.argmin(abs(z-z0))
parmxyt=parm[iz,:,:,:]
parmamp=np.empty((lt))
xprime=np.empty((lt))
for it in range(0,lt):
    xprime[it]=x0+v*tsec[it]           # position of gradient translated to current time
    ix=np.argmin(abs(x-xprime[it]))
    parmamp[it]=np.std(parmxyt[ix,:,it])

# Plot a curve that represents the growth of the fluctuation amplitude
plt.figure()
plt.semilogy(tsec,parmamp)
plt.xlabel("time (s)")
plt.ylabel("amplitude")

# Define a saturation value (with some buffer) and remove elements from the saturated state
satamp=parmamp[-1]
amplimit=0.75*satamp    # linear growth up to some percentage of the saturated state
inds=parmamp<amplimit
tsec_nosat=tsec[inds]
parmamp_nosat=parmamp[inds]

# Find the time of local minimum and remove anything up to that time
itmin=np.argmin(parmamp_nosat)
t_linear=tsec_nosat[itmin:]
parm_linear=parmamp_nosat[itmin:]

# plot just the "linear" regime, as well as the saturation amplitude used
plt.semilogy(t_linear,parm_linear)
plt.xlabel("time (s)")
plt.ylabel("amplitude")
plt.plot(tsec[-1],satamp,"o")

# fit a line to log amplitude
ln_parm=np.log(parm_linear)    # log amplitude data (linear growth only)
p=np.polyfit(t_linear,ln_parm,1)
logslope=p[0]     # highest order coefficient first! Why!
parmfit=np.exp(p[1])*np.exp(logslope*t_linear)

# analytical form of growth rate
ell=5e3
gamma=v/ell

plt.plot(t_linear,parmfit,'.')
plt.legend( ("amplitude", "linear stage", "saturated reference", "log-linear fit") )
plt.title("Emprical $\gamma$ = "+str(logslope)+"; Analytical $\gamma$ = "+str(gamma) )

