#!/usr/bin/env python3
"""
@author: zettergm
"""

import gemini3d.read
from plotcurv import plotcurv2D
from matplotlib.pyplot import show

# load some sample data (2D)
direc = "~/simulations/raid/2Dmidlat_test/"
cfg = gemini3d.read.config(direc)
xg = gemini3d.read.grid(direc)
dat = gemini3d.read.frame(direc, cfg["time"][0], var="v1")

# grid data
plotcurv2D(xg, dat["ne"], lalt=1024, llat=1024)

show()
