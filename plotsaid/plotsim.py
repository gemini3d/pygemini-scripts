#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 20:26:24 2021

load and plot said simulation

@author: zettergm
"""

# imports
import gemini3d.read as read
import gemini3d.plot
from matplotlib.pyplot import show

# load some sample data (3D)
direc = "~/simulations/raid/said_curv_long_allspecies_uneven/"
cfg = read.config(direc)
xg = read.grid(direc)
dat = read.frame(direc, cfg["time"][-1], var="Ti")

# grid data
gemini3d.plot.curv3D_long(xg, dat["Ti"], cfg, lalt=128, llon=128, llat=128)

show()
