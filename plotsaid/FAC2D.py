#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 08:55:32 2022

@author: zettergm
"""

import gemini3d.read
import matplotlib.pyplot as plt
import numpy as np

cfg=gemini3d.read.config("~/simulations/STEVE2D_dist_pot_0.05")
xg=gemini3d.read.grid("~/simulations/STEVE2D_dist_pot_0.05")
y=xg["x3"][2:-2]
dat1=gemini3d.read.frame("~/simulations/STEVE2D_dist_pot_0.05",time=cfg["time"][-1])
dat2=gemini3d.read.frame("~/simulations/STEVE2D_dist_pot_0.5",time=cfg["time"][-1])

J11=np.array(dat1["J1"][400,:,:])
J11=np.squeeze(J11)

J12=np.array(dat2["J1"][400,:,:])
J12=np.squeeze(J12)

plt.figure(num=1,dpi=200)
plt.plot(y[400:500],J11[400:500]/max(J11[400:500]),"*")
plt.plot(y[400:500],J12[400:500]/max(J12[400:500]),'o')
plt.xlabel("y (km)")
plt.ylabel("normalized FAC")
plt.legend( ("Q=0.05","Q=0.5") )