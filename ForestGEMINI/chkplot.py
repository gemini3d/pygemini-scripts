#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 17:34:24 2022

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt

direc="~/simulations/tohoku20113D_lowres_axineu_fclaw_dneu_firsttest/composite/"
filename="20110311_35700.000000.h5"
dat=gemini3d.read.data(direc+filename)
v1=dat["v1"][:,:,24]

plt.figure(dpi=200)
plt.pcolormesh(v1)
plt.colorbar()
plt.show()

