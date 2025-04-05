#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 17:09:09 2025

@author: zettergm
"""

import numpy as np
import struct
import matplotlib.pyplot as plt

direc="/Users/zettergm/Projects/ForestGEMINI/build/examples/figments/"
filename="./gemini_output/end_error.dat"
fid=open(direc+filename,"rb")
datastr=fid.read()
data=np.frombuffer(datastr,dtype=np.float64)
data=np.reshape(data,(16,16,5,21))

ne=data[:,:,3,6]
v1=data[:,:,3,13]
plt.figure(dpi=150)
plt.pcolormesh(ne)
plt.colorbar()

plt.figure(dpi=150)
plt.pcolormesh(v1)
plt.colorbar()