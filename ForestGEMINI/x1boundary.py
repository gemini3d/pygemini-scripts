#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 17:47:04 2024

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
import os

os.environ["GEMINI_CIROOT"]="~/Projects/gemini3d/build/"

direcnew="~/Projects/gemini3d/build/mini2dns_fang/"
direcold="~/Projects/gemini3d/build/test_data/compare/mini2dns_fang/"

cfg=gemini3d.read.config(direcnew)
xg=gemini3d.read.grid(direcnew)
datnew=gemini3d.read.frame(direcnew,cfg["time"][-1])
datold=gemini3d.read.frame(direcold,cfg["time"][-1])

plt.figure()
plt.pcolormesh(datnew["v1"][:,0,:])
plt.colorbar()

plt.figure()
plt.pcolormesh(datold["v1"][:,0,:])
plt.colorbar()

plt.figure()
plt.pcolormesh(datnew["v1"][:,0,:]-datold["v1"][:,0,:])
plt.colorbar()

plt.figure()
plt.plot(datnew["v1"][:,0,0])
plt.plot(datold["v1"][:,0,0])
