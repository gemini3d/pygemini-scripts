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
#x0=-655e3            # initial x-position of trailing edge of patch
#z0=312e3             # hmF2
x0=-85e3
z0=300e3

# Simulation information and grid
#direc="~/simulations/sdcard/GDI_periodic_lowres/"
#direc="~/simulations/sdcard/GDI_periodic_lowres_denspot/"
#direc="~/simulations/sdcard/ONR_Lamarche/GDI_reference/"
direc="~/simulations/sdcard/GDI_periodic_lowres_denspot_1e-6/"
#direc="~/simulations/sdcard/ONR_Lamarche/GDI_reference_hires/"
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

# Initial patch position index
ix0=np.argmin(abs(x-x0))
iz=np.argmin(abs(z-z0))
iy0=ly//2

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
    dat=gemini3d.read.frame(direc,cfg["time"][it],var=[parmlbl,"v2"])
    parm[:,:,:,it]=dat[parmlbl]
    tsec[it]=(cfg["time"][it]-refdate).total_seconds()

    if (it==0):
        v = -cfg["Eyit"]/abs(Bmag)
        
# time series analysis for growth rate
parmxyt=parm[iz,:,:,:]
parmyt=np.empty((ly,lt))
parmamp=np.empty((lt))
xprime=np.empty((lt))
ne0=np.empty((lt))
for it in range(0,lt):
    xprime[it]=x0+v*tsec[it]           # position of gradient translated to current time
    ix=np.argmin(abs(x-xprime[it]))
    parmyt[:,it]=parmxyt[ix,:,it]
    parmamp[it]=np.std(parmxyt[ix,:,it])
    ne0[it]=np.mean(parmxyt[ix,:,it])
#    Gives same results
#    meanparm=np.mean(parmxyt[ix,:,it])
#    parmamp[it]=np.max(parmxyt[ix,:,it]-meanparm)

# Plot a curve that represents the growth of the fluctuation amplitude
plt.figure()
plt.semilogy(tsec,parmamp)
plt.xlabel("time (s)")
plt.ylabel("amplitude")

# Define a saturation value (with some buffer) and remove elements from the saturated state
satamp=parmamp[-1]
#amplimit=0.75*satamp    # linear growth up to some percentage of the saturated state
amplimit=0.5*satamp    # linear growth up to some percentage of the saturated state
inds=parmamp<amplimit
tsec_nosat=tsec[inds]
parmamp_nosat=parmamp[inds]

# Find the time of local minimum and remove anything up to that time
itmin=np.argmin(parmamp_nosat)
#it0=itmin      # 1 min. output
it0=itmin+3    # 10s output
t_linear=tsec_nosat[it0:]
parm_linear=parmamp_nosat[it0:]

# plot just the "linear" regime, as well as the saturation amplitude used
plt.semilogy(t_linear,parm_linear)
plt.xlabel("time (s)")
plt.ylabel("amplitude")
plt.plot(tsec[-1],satamp,"o")

# fit a line to log amplitude
ln_parm=np.log(parm_linear)    # log amplitude data (linear growth only)
p=np.polyfit(t_linear,ln_parm,1)
logslope=p[0]
parmfit=np.exp(p[1])*np.exp(logslope*t_linear)

# analytical form of growth rate
colden=np.empty((lx,ly))
for ix in range(0,lx):
    for iy in range(0,ly):
        colden[ix,iy]=np.trapz(parm[:,ix,iy,it0],z)
        
dNdx,dNdy=np.gradient(colden,x,y)

ell=colden/dNdx
ix0_it0=np.argmin(abs(x-xprime[it0]))
#gamma=v/ell[ix0_itmin,iy0]
gamma=v/np.mean(ell[ix0_it0,:])

# # Initial patch position index, but take from after when simulation has settled
# ix0_itmin=np.argmin(abs(x-xprime[itmin]))
# parmslice=parm[iz,:,ly//2,itmin]
# dndx=np.gradient(parmslice,x)
# ell=parmslice[ix0_itmin]/dndx[ix0_itmin]
# gamma=v/ell

plt.plot(t_linear,parmfit,'^')
plt.plot(tsec,ne0,"--")
plt.plot(tsec,0.1*ne0,":")
plt.legend( ("amplitude", "linear stage", "saturated reference", "log-linear fit","background","nonlinearity") )
plt.title("Emprical $\gamma$ = "+str(logslope)+"; Analytical $\gamma$ = "+str(gamma) )

# recompute the conductivities
import gemini3d.conductivity
import os
os.environ["GEMINI_ROOT"]="~/Projects/gemini3d/build/_deps/msis-build/"
dat=gemini3d.read.frame(direc,cfg["time"][0])
sigP,sigH,_,_,_,_,_ = gemini3d.conductivity.conductivity_reconstruct(refdate, dat, cfg, xg)

#plt.figure()
plt.subplots(1,2)
plt.subplot(1,2,1)
plt.semilogx(parm[:,ix0,iy0,0],z/1e3)
plt.xlabel("plasma density (m$^{-3}$)")
plt.ylabel("altitud (km)")
plt.subplot(1,2,2)
plt.semilogx(sigP[:,ix0,iy0],z/1e3,abs(sigH[:,ix0,iy0]),z/1e3)
plt.legend(("Pedersen","Hall"))
plt.xlabel("conductance (mhos)")
plt.ylabel("altitud (km)")