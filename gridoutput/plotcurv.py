#!/usr/bin/env python3
"""
@author: zettergm
"""

from __future__ import annotations
import typing as T

from matplotlib.pyplot import figure
import xarray

from gemini3d.grid.gridmodeldata import model2magcoords,model2geogcoords


def plotcurv3D(
    xg: dict[str, T.Any],
    parm: xarray.DataArray,
    cfg: dict[str, T.Any],
    lalt: int = 256,
    llon: int = 256,
    llat: int = 256,
    coord: str = "geomagnetic"
):
    """plot dipole grid data vs. alt,lon,lat"""

    # grid data; wasteful and should only do a slice at a time???
    if coord=="geomagnetic":  
        alti, loni, lati, parmi = model2magcoords(xg, parm, lalt, llon, llat)
        lonlbl="mlon"
        latlbl="mlat"
    elif coord=="geographic":
        alti, loni, lati, parmi = model2geogcoords(xg, parm, lalt, llon, llat, wraplon=True)
        lonlbl="glon"
        latlbl="glat"
    else:
        print("WARNING:  defaulting to geomagnetic sampling...")
        alti, loni, lati, parmi = model2magcoords(xg, parm, lalt, llon, llat)
        lonlbl="mlon"
        latlbl="mlat"

    # define slices indices
    altref = 300e3
    ialt = abs(alti - altref).argmin()
    lonavg=loni.mean()
    ilon = abs(loni - lonavg).argmin()
    latavg=lati.mean()
    ilat = abs(lati - latavg).argmin()

    # plot various slices through the 3D domain
    fg = figure()
    axs = fg.subplots(1, 3)

    ax = axs[0]
    h = ax.pcolormesh(loni, alti / 1e3, parmi[:, :, ilat], shading="nearest")
    ax.set_xlabel(lonlbl)
    ax.set_ylabel("alt")
    fg.colorbar(h, ax=ax)

    ax = axs[1]
    h = ax.pcolormesh(loni, lati, parmi[ialt, :, :].transpose(), shading="nearest")
    ax.set_xlabel(lonlbl)
    ax.set_ylabel(latlbl)
    fg.colorbar(h, ax=ax)

    ax = axs[2]
    ax.pcolormesh(lati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
    ax.set_xlabel(latlbl)
    ax.set_ylabel("alt")
    fg.colorbar(h, ax=ax)


# alt,lon plot for 2D dipole data
def plotcurv2D(xg: dict[str, T.Any], parm: xarray.DataArray, lalt: int = 512, llat: int = 512):
    # grid data
    alti, loni, lati, parmi = model2magcoords(xg, parm, lalt, 1, llat)

    # define slices indices, for 2D there is only one longitude index
    ilon = 0

    # plot the meridional slice
    fg = figure()
    ax = fg.gca()
    h = ax.pcolormesh(lati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
    ax.set_xlabel("mlat")
    ax.set_ylabel("alt")
    fg.colorbar(h, ax=ax)
