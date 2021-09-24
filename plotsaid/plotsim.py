#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 20:26:24 2021

load and plot said simulation

@author: zettergm
"""

# imports
import gemini3d.read as read
import gemini3d.plot.curvilinear
import matplotlib.pyplot as plt

# load some sample data (3D)
direc = "~/simulations/raid/said_curv_long_allspecies_uneven/"
cfg = read.config(direc)
xg = read.grid(direc)
dat = read.frame(direc, cfg["time"][-1], var="Ti")

# grid data
fg=plt.figure()
fg,ax=gemini3d.plot.curvilinear.curv3d_long(cfg=cfg,xg=xg,parm=dat["Ti"],fg=fg)
ax[0].set_ylim(0,600)
ax[1].set_aspect('equal')
ax[2].set_ylim(0,600)
plt.show(block=False)
