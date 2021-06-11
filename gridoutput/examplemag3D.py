#!/usr/bin/env python3
"""
@author: zettergm
"""

# imports
import gemini3d.read as read
from plotcurv import plotcurv3D
from matplotlib.pyplot import show

# load some sample data (3D)
direc = "~/simulations/raid/tohoku20113D_lowres_2Daxisneu"
cfg = read.config(direc)
xg = read.grid(direc)
dat = read.frame(direc, cfg["time"][-1], var="v1")

# grid data
plotcurv3D(xg, dat["v1"], cfg, "$v_1$ m/s", lalt=256, llon=256, llat=256)

show()
