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
direc = "~/simulations/tohoku20113D_lowres_2Daxisneu_CI"
cfg = read.config(direc)
xg = read.grid(direc)
dat = read.frame(direc, cfg["time"][-1], var="v1")

# grid different slices, then plot
parm=dat["v1"]
parmlabel="$v_1$ m/s"

[alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 256, 1, 256)
fg = plt.figure()
ax = fg.gca()
h=ax.pcolormesh(mlati, alti / 1e3, parmi[:, 0, :], shading="nearest")
ax.set_xlabel("mlat")
ax.set_ylabel("alt")
cbar=fg.colorbar(h, ax=ax)
cbar.set_label(parmlabel)
show(block=False)

[alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 1, 256, 256,altlims=(300e3))
fg = plt.figure()
ax = fg.gca()
h = ax.pcolormesh(mloni, mlati, parmi[0, :, :].transpose(), shading="nearest")
ax.set_xlabel("mlon")
ax.set_ylabel("mlat")
cbar=fg.colorbar(h, ax=ax)
cbar.set_label(parmlabel)
show(block=False)

[alti, mloni, mlati, parmi] = model2magcoords(xg, parm, 256, 256, 1, mlatlims=(29))
fg = plt.figure()
ax = fg.gca()
h = ax.pcolormesh(mloni, alti / 1e3, parmi[:, :, 0], shading="nearest")
ax.set_xlabel("mlon")
ax.set_ylabel("alt")
cbar=fg.colorbar(h, ax=ax)
cbar.set_label(parmlabel)
show(block=False)

