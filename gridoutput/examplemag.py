#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 10:34:45 2021

@author: zettergm
"""

# imports
from gemini3d.grid.gridmodeldata import model2magcoords
import gemini3d.read
import matplotlib.pyplot as plt

# load some sample data
direc="~/simulations/tohoku20113D_lowres_2Daxisneu_CI/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,cfg["time"][-1])

# grid data
parm=dat["v1"]

[alti,mloni,mlati,parmi]=model2magcoords(xg,parm,100,100,100)

# plot
