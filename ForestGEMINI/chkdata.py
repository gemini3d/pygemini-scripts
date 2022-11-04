#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 20:17:24 2022

@author: zettergm
"""

import h5py
import matplotlib.pyplot as plt

# grab the data
filename="/Users/zettergm/dump_nonfinite_output_worker_0.h5"
f = h5py.File(filename,"r")
vs1=f["vs1"][:]
ns=f["ns"][:]
vs1=vs1.transpose([3,2,1,0])
ns=ns.transpose([3,2,1,0])
f.close()

# try to plot
plt.figure()
plt.pcolormesh(vs1[:,:,10,0])
c=plt.colorbar()
plt.clim([-1000,1000])
plt.show()

plt.figure()
plt.pcolormesh(ns[:,:,10,0])
c=plt.colorbar()
plt.clim([0,3e11])
plt.show()

