#!/usr/bin/env python3
"""
@author: zettergm
"""

# imports
from gemini3d.grid.gridmodeldata import model2magcoords
import matplotlib.pyplot as plt
import xarray


def plotcurv3D(xg, parm: xarray.DataArray, cfg, parmlabel, lalt=256, llon=256, llat=256):
    """plot dipole data vs. alt,lon,lat"""

    # define slices indices
    altref = 300e3
    
    fg = plt.figure()
    axs = fg.subplots(1, 3)
    
    [alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 256, 1, 256, mlonlims=(cfg["sourcemlon"]))    
    ax = axs[0]
    h=ax.pcolormesh(mlati, alti / 1e3, parmi[:, 0, :], shading="nearest")
    ax.set_xlabel("mlat (deg)")
    ax.set_ylabel("alt (km)")
    cbar=fg.colorbar(h, ax=ax)
    cbar.set_label(parmlabel)
    plt.show(block=False)
    
    [alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 1, 256, 256,altlims=(altref))
    ax = axs[1]
    h = ax.pcolormesh(mloni, mlati, parmi[0, :, :].transpose(), shading="nearest")
    ax.set_xlabel("mlon (deg)")
    ax.set_ylabel("mlat (deg)")
    cbar=fg.colorbar(h, ax=ax)
    cbar.set_label(parmlabel)
    plt.show(block=False)
    
    [alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 256, 256, 1, mlatlims=(cfg["sourcemlat"]))
    ax = axs[2]
    h = ax.pcolormesh(mloni, alti / 1e3, parmi[:, :, 0], shading="nearest")
    ax.set_xlabel("mlon (deg)")
    ax.set_ylabel("alt (km)")
    cbar=fg.colorbar(h, ax=ax)
    cbar.set_label(parmlabel)
    plt.show(block=False)


def plotcurv2D(xg, parm, parmlabel,lalt=512, llat=512):
    """ alt,lon plot for 2D dipole data"""
    
    # grid data
    [alti, mloni, mlati, parmi] = model2magcoords(xg, parm, lalt, 1, llat)

    # define slices indices, for 2D there is only one longitude index
    ilon = 0

    # plot the meridional slice
    fg = plt.figure()
    ax = fg.gca()
    h = ax.pcolormesh(mlati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
    ax.set_xlabel("mlat (deg)")
    ax.set_ylabel("alt (km)")
    cbar=fg.colorbar(h, ax=ax)
    cbar.set_label(parmlabel)
