#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:20:00 2022

Compare simulations run with geomagnetic vs. geographic interpolation of input
MAGIC data...

@author: zettergm
"""

# imports
import gemini3d.read as read
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2geogcoords

# load some sample data (3D)
direc1 = "~/simulations/raid/tohoku20113D_lowres_3Dneu_f90/"
direc2 = "~/simulations/raid/tohoku20113D_lowres_3Dneu_geogfix/"
cfg = read.config(direc1)
xg = read.grid(direc1)
parm="v1"
dat1 = read.frame(direc1, cfg["time"][-1], var=parm)
dat2 = read.frame(direc2, cfg["time"][-1], var=parm)

# produce gridding datasets from model
lalt=128; llon=256; llat=256;
glonlims=[498,507];
glatlims=[32,43];
altlims=[0,600e3];

# grid model output
galti, gloni, glati, parm1gi = model2geogcoords(xg, dat1[parm], lalt, llon, llat, 
                                               altlims=altlims, glonlims=glonlims, 
                                               glatlims=glatlims, wraplon=True)
galti, gloni, glati, parm2gi = model2geogcoords(xg, dat2[parm], lalt, llon, llat, 
                                               altlims=altlims, glonlims=glonlims, 
                                               glatlims=glatlims, wraplon=True)

# define slices indices
altref = 300e3
ialt = abs(galti - altref).argmin()

# messy plot code
plt.subplots(1,2)
plt.subplot(1,2,1)
plt.pcolormesh(gloni,glati,parm1gi[ialt,:,:].transpose())
plt.xlabel("glon")
plt.ylabel("glat")
plt.title("MAGIC as geomagnetically aligned")
plt.colorbar()
plt.subplot(1,2,2)
plt.pcolormesh(gloni,glati,parm2gi[ialt,:,:].transpose())
plt.xlabel("glon")
plt.ylabel("glat")
plt.title("MAGIC as geographically aligned")
plt.colorbar()
