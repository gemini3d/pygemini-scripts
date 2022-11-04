#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 19:46:12 2022

@author: zettergm
"""

import h5py
import gemini3d.read

direc="/Users/zettergm/simulations/raid/RISR_staging_data_highres/"
xg=gemini3d.read.grid(direc)
z=xg["x1"][2:-2]
x=xg["x2"][2:-2]
y=xg["x3"][2:-2]

f = h5py.File(direc+"/inputs/gridxyz.h5","w")
f.create_dataset("/z",data=z)
f.create_dataset("/x",data=x)
f.create_dataset("/y",data=y)
f.close()
