#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 17:28:02 2025

@author: zettergm
"""

import gemini3d.read
import gemini3d.magtools
import matplotlib.pyplot as plt
import os

os.environ["GEMINI_CIROOT"]="~/Projects/gemini3d/build/"

direc="/Users/zettergm/simulations/sdcard/arcs/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
mag=gemini3d.magtools.magframe(direc+"/magfields/20170302_27030.000000.h5")

plt.figure()
plt.pcolormesh(mag["mlon"],mag["mlat"],mag["Bphi"][0,:,:].transpose())
plt.colorbar()