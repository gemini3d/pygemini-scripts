#!/usr/bin/env python3
"""
@author: zettergm
"""

import gemini3d.read
from plotcurv import plotcurv2D
from matplotlib.pyplot import show
from gemini3d.grid.gridmodeldata import model2magcoords

# load some sample data (2D)
direc = "~/simulations/raid/2Dmidlat_test/"
cfg = gemini3d.read.config(direc)
xg = gemini3d.read.grid(direc)
dat = gemini3d.read.frame(direc, cfg["time"][0])

# grid data
lalt = 1024
llat = 1024
llon = 1
parm = dat["v1"]
alti, mloni, mlati, parmi = model2magcoords(xg, parm, lalt, llon, llat)

# plot data
plotcurv2D(xg, dat["ne"], lalt=1024, llat=1024)
show(block=False)
