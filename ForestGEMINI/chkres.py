#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:20:57 2023

Create a grid for the AIRWaveS misty picture experiment.  

@author: zettergm
"""

import matplotlib.pyplot as plt
import gemini3d.grid.tilted_dipole
import gemini3d.read
import numpy as np
import gemini3d.grid.gridmodeldata
import xarray

flagplot=False

cfg=gemini3d.read.config("~/Projects/ForestGemini/build/examples/figments/misty_NM_256/inputs/config.nml")
xg=gemini3d.grid.tilted_dipole.tilted_dipole3d(cfg)
#xg=gemini3d.grid.tilted_dipole.tilted_dipole3d_NUx2(cfg)

dl1=xg["dx1h"]*xg["h1"][2:-2,0,0]/1e3
dl1_var=xg["dx1h"]*xg["h1"][2:-2,-1,-1]/1e3
alt=xg["alt"][:,0,0]/1e3
alt_var=xg["alt"][:,-1,-1]/1e3

# diagnostic for parallel to B resolution
if flagplot:
    plt.figure(dpi=150)
    plt.plot(dl1,alt,dl1_var,alt_var)
    plt.xlabel("differential length (km)")
    plt.ylabel("altitude (km)")

# compute differential lengths across entire grid, level 0 refinement
dl1=np.empty(xg["lx"])
for i in range(0,xg["lx"][1]):
    for j in range(0,xg["lx"][2]):
        dl1[:,i,j] = xg["dx1h"]*xg["h1"][2:-2,i+2,j+2]/1e3    # offset due to ghost cells
        
dl2=np.empty(xg["lx"])
for k in range(0,xg["lx"][0]):
    for j in range(0,xg["lx"][2]):
        dl2[k,:,j]=xg["dx2h"]*xg["h2"][k+2,2:-2,j+2]/1e3   # offset for ghost cells

dl3=np.empty(xg["lx"])
for k in range(0,xg["lx"][0]):
    for i in range(0,xg["lx"][1]):
        dl3[k,i,:]=xg["dx3h"]*xg["h2"][k+2,i+2,2:-2]/1e3   # offset for ghost cells

# sample differential lengths at fixed heights of interest to AIRWaveS
thlims=np.array([np.min(xg["theta"]), np.max(xg["theta"]) ])
philims=np.array([np.min(xg["phi"]), np.max(xg["phi"]) ])
mlonlims=philims*180/np.pi
mlatlims=[90-180/np.pi*thlims[1], 90-180/np.pi*thlims[0]]
altlims=np.array( [120e3, 300e3] )
alti,mloni,mlati,dl1i = gemini3d.grid.gridmodeldata.model2magcoords(xg,
                            xarray.DataArray(dl1),2,256,256,altlims,mlonlims,mlatlims)
alti,mloni,mlati,dl2i = gemini3d.grid.gridmodeldata.model2magcoords(xg,
                            xarray.DataArray(dl2),2,256,256,altlims,mlonlims,mlatlims)
alti,mloni,mlati,dl3i = gemini3d.grid.gridmodeldata.model2magcoords(xg,
                            xarray.DataArray(dl3),2,256,256,altlims,mlonlims,mlatlims)
# alti,mloni,mlati,dl1i = gemini3d.grid.gridmodeldata.model2magcoords(xg,
#                             xarray.DataArray(dl1),256,256,256)
# alti,mloni,mlati,dl2i = gemini3d.grid.gridmodeldata.model2magcoords(xg,
#                             xarray.DataArray(dl2),256,256,256)
# alti,mloni,mlati,dl3i = gemini3d.grid.gridmodeldata.model2magcoords(xg,
#                             xarray.DataArray(dl3),256,256,256)

plt.subplots(2,3)

plt.subplot(2,3,1)
plt.pcolormesh(mloni,mlati,dl1i[0,:,:].transpose())
plt.colorbar()
plt.title("$dl_1$ (km) at 120 km altitude")
plt.subplot(2,3,4)
plt.pcolormesh(mloni,mlati,dl1i[1,:,:].transpose())
plt.colorbar()
plt.title("$dl_1$ (km) at 300 km altitude")

plt.subplot(2,3,2)
plt.pcolormesh(mloni,mlati,dl2i[0,:,:].transpose())
plt.colorbar()
plt.title("$dl_2$ (km), level 0 at 120 km altitude")
plt.subplot(2,3,5)
plt.pcolormesh(mloni,mlati,dl2i[1,:,:].transpose())
plt.colorbar()
plt.title("$dl_2$ (km), level 0 at 300 km altitude")

plt.subplot(2,3,3)
plt.pcolormesh(mloni,mlati,dl3i[1,:,:].transpose())
plt.colorbar()
plt.title("$dl_3$ (km), level 0 at 120 km altitude")
plt.subplot(2,3,6)
plt.pcolormesh(mloni,mlati,dl3i[1,:,:].transpose())
plt.colorbar()
plt.title("$dl_3$ (km), level 0 at 300 km altitude")

###############################################################################
#  FIGMENTS/ForestGEMINI misty picture test, 3Dx
###############################################################################
#
# For 8x8 patches and level 3 initial refinement (or mi=mj=8 and lvl 0 initial refine) 
#   we are going to need an additional 4 levels of refinement
#
# The goal is ~1km resolution (max) and a grid extent covering:  320km radius in x-y plane
#   This corresponds to about 8 degrees mlat/mlon
###############################################################################


###############################################################################
#  CGCAM testing
###############################################################################
#   Targetting resolution of 4x4x4 km means we need a grid of about
#     512**3; 384**3 may also be acceptable for initial tests
###############################################################################


###############################################################################
#  FIGMENTS/ForestGEMINI misty picture test, 3Dx
###############################################################################
#
# For 16x16 patches with 8x6x16 blocks and level 0 initial refine
#
# The goal is ~1km resolution (max) and a grid extent covering:  320km radius in x-y plane
#   This corresponds to about 8 degrees mlat/mlon
# 
###############################################################################

