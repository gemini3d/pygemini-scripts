#!/usr/bin/env python3
"""
@author: zettergm
"""

from __future__ import annotations
import typing as T

from matplotlib.pyplot import figure
import xarray

from gemini3d.grid.gridmodeldata import model2magcoords, model2geogcoords



def plotcurv3D(
    xg: dict[str, T.Any],
    parm: xarray.DataArray,
    cfg: dict[str, T.Any],
    lalt: int = 256,
    llon: int = 256,
    llat: int = 256,
    coords: str = 'geomag'
):
    """plot dipole data vs. alt,lon,lat"""
    if coords == 'geomag':
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
        fg = figure(figsize=(14,6)) #change fig size
        axs = fg.subplots(1, 3)
        fg.subplots_adjust(left=.2, wspace=.3,right=1.2)
        
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
    
    elif coords == 'geog':
        # grid data; wasteful and should only do a slice at a time???
        #alti, mloni, mlati, parmi = model2magcoords(xg, parm, lalt, llon, llat)
        alti, gloni, glati, parmi = model2geogcoords(xg, parm, lalt, llon, llat)
        # define slices indices
        altref = 300e3
        ialt = abs(alti - altref).argmin()
        lonavg = cfg["glon"]
        ilon = abs(gloni - lonavg).argmin()
        latavg = cfg["glat"]
        ilat = int(glati.size/2)

        # plot various slices through the 3D domain
        fg = figure(figsize=(14,6)) #change fig size
        axs = fg.subplots(1, 3)
        fg.subplots_adjust(left=.2, wspace=.3,right=1.2)
        
        ax = axs[0]
        h = ax.pcolormesh(gloni, alti / 1e3, parmi[:, :, ilat], shading="nearest")
        ax.set_xlabel("glon")
        ax.set_ylabel("alt")
        fg.colorbar(h, ax=ax)
    
        ax = axs[1]
        h = ax.pcolormesh(gloni, glati, parmi[ialt, :, :].transpose(), shading="nearest")
        ax.set_xlabel("glon")
        ax.set_ylabel("glat")
        fg.colorbar(h, ax=ax)
    
        ax = axs[2]
        ax.pcolormesh(glati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
        ax.set_xlabel("glat")
        ax.set_ylabel("alt")
        fg.colorbar(h, ax=ax)
    
    else:
        print('"'+coords+'" coordinate input not recognized')

# alt,lon plot for 2D dipole data
def plotcurv2D(xg: dict[str, T.Any], parm: xarray.DataArray, lalt: int = 512, llat: int = 512):
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
