#!/usr/bin/env python3
"""
@author: zettergm
"""

import typing as T
from gemini3d.grid.gridmodeldata import model2magcoords
from matplotlib.pyplot import figure
import xarray


def plotcurv3D(
    xg,
    parm,
    cfg,
    lalt: int = 256,
    llon: int = 256,
    llat: int = 256,
):
    """plot dipole data vs. alt,lon,lat"""

    # grid data; wasteful and should only do a slice at a time???
    alti, mloni, mlati, parmi = model2magcoords(xg, parm, lalt, llon, llat)

    # define slices indices
    altref = 300e3
    ialt = abs(alti - altref).argmin()
    lonavg = cfg["sourcemlon"]
    ilon = abs(mloni - lonavg).argmin()
    latavg = cfg["sourcemlat"]
    ilat = abs(mlati - latavg).argmin()

    # plot various slices through the 3D domain
    fg = figure()
    axs = fg.subplots(1, 3)

    ax = axs[0]
    h = ax.pcolormesh(mloni, alti / 1e3, parmi[:, :, ilat], shading="nearest")
    ax.set_xlabel("mlon")
    ax.set_ylabel("alt")
    fg.colorbar(h, ax=ax)

    ax = axs[1]
    h = ax.pcolormesh(mloni, mlati, parmi[ialt, :, :].transpose(), shading="nearest")
    ax.set_xlabel("mlon")
    ax.set_ylabel("mlat")
    fg.colorbar(h, ax=ax)

    ax = axs[2]
    ax.pcolormesh(mlati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
    ax.set_xlabel("mlat")
    ax.set_ylabel("alt")
    fg.colorbar(h, ax=ax)


# alt,lon plot for 2D dipole data
def plotcurv2D(xg, parm, lalt: int = 512, llat: int = 512):
    # grid data
    alti, mloni, mlati, parmi = model2magcoords(xg, parm, lalt, 1, llat)

    # define slices indices, for 2D there is only one longitude index
    ilon = 0

    # plot the meridional slice
    fg = figure()
    ax = fg.gca()
    h = ax.pcolormesh(mlati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
    ax.set_xlabel("mlat")
    ax.set_ylabel("alt")
    fg.colorbar(h, ax=ax)
