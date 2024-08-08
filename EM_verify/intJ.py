#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 08:08:02 2024

@author: zettergm
"""

import gemini3d.read
import numpy as np

# load data
direc="~/simulations/sdcard/aurora_EISCAT3D_centered/"
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
dat=gemini3d.read.frame(direc,time=cfg["time"][15])

# grid geometric information
x1=xg["x1"][2:-2]
x2=xg["x2"][2:-2]
x3=xg["x3"][2:-2]
lx1=x1.size
lx2=x2.size
lx3=x3.size
h1=xg["h1"][2:-2,2:-2,2:-2]
h2=xg["h2"][2:-2,2:-2,2:-2]
h3=xg["h3"][2:-2,2:-2,2:-2]
dx1=xg["dx1h"]    # cell lengths
dx2=xg["dx2h"]
dx3=xg["dx3h"]

# current density from the simulation
J1=dat["J1"]
J2=dat["J2"]
J3=dat["J3"]

# compute total current through each of the six coordinate bounding surfaces 
#     x1[bottom,top], x2[left,right], x3[bwd,fwd].  As long as the data are
#     cell-centered this is equivalent to a 2D trapezoidal rule.  
#
# bottom
I = np.empty((6))
I[0]=0
for i2 in range(lx2):
    for i3 in range(lx3):
        I[0] += J1[0,i2,i3]*h2[0,i2,i3]*h3[0,i2,i3]*dx2[i2]*dx3[i3]

# top, minus due to surf. normal in -x1 direction
I[1]=0
for i2 in range(lx2):
    for i3 in range(lx3):
        I[1] -= J1[-1,i2,i3]*h2[-1,i2,i3]*h3[-1,i2,i3]*dx2[i2]*dx3[i3]

# left
I[2]=0
for i1 in range(lx1):
    for i3 in range(lx3):
        I[2] += J2[i1,0,i3]*h1[i1,0,i3]*h3[i1,0,i3]*dx1[i2]*dx3[i3]

# right
I[3]=0
for i1 in range(lx1):
    for i3 in range(lx3):
        I[3] -= J2[i1,-1,i3]*h1[i1,-1,i3]*h3[i1,-1,i3]*dx1[i2]*dx3[i3]

# bwd
I[4]=0
for i1 in range(lx1):
    for i2 in range(lx2):
        I[4] += J3[i1,i2,0]*h1[i1,i2,0]*h2[i1,i2,0]*dx1[0]*dx2[0]
        
I[5]=0
for i1 in range(lx1):
    for i2 in range(lx2):
        I[5] -= J3[i1,i2,-1]*h1[i1,i2,-1]*h2[i1,i2,-1]*dx1[0]*dx2[0]        

print("mean(|I|):  ",np.mean(abs(I)),"; net I:  ",np.sum(I))