#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 15:38:19 2023

@author: zettergm
"""

# Imports
import gemini3d.read
import numpy as np
import matplotlib.pyplot as plt

# Create or read a reference uniform grid commensurate with aurora_EISCAT3D_eq
direc="~/simulations/ssd/aurora_EISCAT3D_eq/"
cfg=gemini3d.read.config(direc)
xgref=gemini3d.read.grid(direc)

# Extract needed data from grid dict
x1=xgref["x1"][2:-2]
x2=xgref["x2"][2:-2]
x3=xgref["x3"][2:-2]
dx1=xgref["dx1b"][1:-2]
dx2=xgref["dx2b"][1:-2]
dx3=xgref["dx3b"][1:-2]
h1=xgref["h1"][2:-2,2:-2,2:-2]
h2=xgref["h2"][2:-2,2:-2,2:-2]
h3=xgref["h3"][2:-2,2:-2,2:-2]

# Define a reference local position along the field line and in longitude
i1=x1.size-1
i3=x3.size//2

# Compute differential lengths for grid
dl2=h2[i1,:,i3]*dx2

# Quick plot of lengths
plt.figure(dpi=150)
plt.plot(x2,dl2/1e3)
plt.xlabel("$x_2$")
plt.ylabel("differential lenght (km)")

# Fit a polynomial to differential length as a function of x2 coordinate
pfit=np.polyfit(x2,dl2,16)
pval=np.polyval(pfit,x2)

# Add fit to plot to evaluate goodness
plt.plot(x2,pval/1e3)
plt.show()

