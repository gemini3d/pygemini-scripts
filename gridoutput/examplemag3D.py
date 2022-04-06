#!/usr/bin/env python3
"""
@author: zettergm
"""

# imports
import gemini3d.read as read
from plotcurv import plotcurv3D
from matplotlib.pyplot import show
from gemini3d.grid.gridmodeldata import model2magcoords,model2geogcoords

# load some sample data (3D)
#direc = "~/simulations/raid/tohoku20112D_medres/"
direc = "~/simulations/raid/aurora_EISCAT3D_simple_wide/"
cfg = read.config(direc)
xg = read.grid(direc)
parm="Ti"
dat = read.frame(direc, cfg["time"][-1], var=parm)

# these plotting functions will internally grid data
print("Plotting...")
plotcurv3D(xg, dat[parm], cfg, lalt=128, llon=128, llat=128, coord="geographic")

# produce gridding datasets from model
lalt=128; llon=128; llat=128;

# regrid data in geographic
print("Sampling in geographic coords...")
galti, gloni, glati, parmgi = model2geogcoords(xg, dat[parm], lalt, llon, llat, wraplon=True)

# regrid in geomagnetic
print("Sampling in geomagnetic coords...")
malti, mloni, mlati, parmmi = model2magcoords(xg, dat[parm], lalt, llon, llat)

# bring up plot
show(block=False)

