#!/usr/bin/env python3
"""
@author: zettergm
"""

# imports
import gemini3d.read as read
from plotcurv import plotcurv3D
from matplotlib.pyplot import show

# load some sample data (3D)
direc = "~/simulations/raid/tohoku20112D_medres/"
cfg = read.config(direc)
xg = read.grid(direc)
dat = read.frame(direc, cfg["time"][-1], var="v1")

# grid data
plotcurv3D(xg, dat["v1"], cfg, lalt=128, llon=128, llat=128)

show()
