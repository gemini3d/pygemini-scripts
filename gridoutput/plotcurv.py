#!/usr/bin/env python3
"""
@author: zettergm
"""

# imports
from gemini3d.grid.gridmodeldata import model2magcoords
from matplotlib.pyplot import figure
import numpy as np
import xarray


def plotcurv3D(xg, parm: xarray.DataArray, cfg, parmlabel, lalt=256, llon=256, llat=256):
    """plot dipole data vs. alt,lon,lat"""

    # grid data; wasteful and should only do a slice at a time???
    [alti, mloni, mlati, parmi] = model2magcoords(xg, parm, lalt, llon, llat)

    # define slices indices
    altref = 300e3
    ialt = np.argmin(abs(alti - altref))
    lonavg = cfg["sourcemlon"]
    ilon = np.argmin(abs(mloni - lonavg))
    latavg = cfg["sourcemlat"]
    ilat = np.argmin(abs(mlati - latavg))

    # plot various slices through the 3D domain
    fg = figure()
    axs = fg.subplots(1, 3)

    ax = axs[0]
    h=ax.pcolormesh(mlati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
    ax.set_xlabel("mlat")
    ax.set_ylabel("alt")
    cbar=fg.colorbar(h, ax=ax)
    cbar.set_label(parmlabel)

    ax = axs[1]
    h = ax.pcolormesh(mloni, mlati, parmi[ialt, :, :].transpose(), shading="nearest")
    ax.set_xlabel("mlon")
    ax.set_ylabel("mlat")
    cbar=fg.colorbar(h, ax=ax)
    cbar.set_label(parmlabel)

    ax = axs[2]
    h = ax.pcolormesh(mloni, alti / 1e3, parmi[:, :, ilat], shading="nearest")
    ax.set_xlabel("mlon")
    ax.set_ylabel("alt")
    cbar=fg.colorbar(h, ax=ax)
    cbar.set_label(parmlabel)

# alt,lon plot for 2D dipole data
def plotcurv2D(xg, parm, parmlabel,lalt=512, llat=512):
    # grid data
    [alti, mloni, mlati, parmi] = model2magcoords(xg, parm, lalt, 1, llat)

    # define slices indices, for 2D there is only one longitude index
    ilon = 0

    # plot the meridional slice
    fg = figure()
    ax = fg.gca()
    h = ax.pcolormesh(mlati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
    ax.set_xlabel("mlat")
    ax.set_ylabel("alt")
    cbar=fg.colorbar(h, ax=ax)
    cbar.set_label(parmlabel)
