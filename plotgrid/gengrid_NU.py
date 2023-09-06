#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:24:53 2023

Generate a grid using the nonuniform mesh creation function

@author: zettergm
"""

from gemini3d.grid.tilted_dipole import tilted_dipole3d_NUx2
import matplotlib.pyplot as plt

# %% generate a 3D grid
cfg = {
    "dtheta": 15,
    "dphi": 110,
    "lp": 96,
    "lq": 256,
    "lphi": 64,
    "altmin": 80e3,
    "glat": 70.22,
    "glon": -5.0,
    "gridflag": 0,
}
xg = tilted_dipole3d_NUx2(cfg)

# check the differential lengths
dl2=xg["dx2b"][1:-2]*xg["h2"][-1,2:-2,32]
plt.figure(dpi=150)
plt.plot(xg["x2"][2:-2],dl2)
plt.xlabel("$x_2$")
plt.ylabel("$dl_2$")


