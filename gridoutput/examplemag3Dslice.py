#!/usr/bin/env python3
"""
@author: zettergm
"""

# imports
import gemini3d.read as read
from plotcurv import plotcurv3D
from matplotlib.pyplot import show
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2magcoords

# load some sample data (3D)
direc = "~/simulations/raid/tohoku20113D_lowres_2Daxisneu"
cfg = read.config(direc)
xg = read.grid(direc)
dat = read.frame(direc, cfg["time"][-1], var="v1")

# grid different slices
parm=dat["v1"]
parmlabel="$v_1$ m/s"
[alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 256, 1, 256)

# plot data
#plotcurv3D(xg, dat["v1"], cfg, "$v_1$ m/s", lalt=256, llon=1, llat=256)
fg = plt.figure()
ax = fg.gca()
h=ax.pcolormesh(mlati, alti / 1e3, parmi[:, 0, :], shading="nearest")
ax.set_xlabel("mlat")
ax.set_ylabel("alt")
cbar=fg.colorbar(h, ax=ax)
cbar.set_label(parmlabel)
show(block=False)


[alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 1, 256, 256)

fg = plt.figure()
ax = fg.gca()
h = ax.pcolormesh(mloni, mlati, parmi[0, :, :].transpose(), shading="nearest")
ax.set_xlabel("mlon")
ax.set_ylabel("mlat")
cbar=fg.colorbar(h, ax=ax)
cbar.set_label(parmlabel)
show(block=False)

[alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 256, 256, 1)

fg = plt.figure()
ax = fg.gca()
h = ax.pcolormesh(mloni, alti / 1e3, parmi[:, :, 0], shading="nearest")
ax.set_xlabel("mlon")
ax.set_ylabel("alt")
cbar=fg.colorbar(h, ax=ax)
cbar.set_label(parmlabel)
show(block=False)

