#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:23:02 2024

@author: zettergm
"""

import h5py
import matplotlib.pyplot as plt
import numpy

direc1="/Users/zettergm/simulations/ssd/misty_NM_256_quasistatic/gemini_output_hdf5/"
direc2="/Users/zettergm/simulations/ssd/misty_NM_256_quasistatic_noenerg/gemini_output_hdf5/"
filename="fort_frame_0014.vtu.hdf5"

f1=h5py.File(direc1+filename, "r")
f2=h5py.File(direc2+filename, "r")

parmlbls=f1["parmlbls"][:]
parmsi=f1["parmi"][:]
v11=parmsi[:,:,:,1]
ne1=parmsi[:,:,:,0]
z=f1["x1i"][:]

parmlbls=f2["parmlbls"][:]
parmsi=f2["parmi"][:]
v12=parmsi[:,:,:,1]
ne2=parmsi[:,:,:,0]

dv1=v12-v11
dne=ne2-ne1


ialt1=numpy.argmin(abs(z-110e3))
ialt2=numpy.argmin(abs(z-200e3))


##### Velocity comparison
plt.subplots(2,3,dpi=150)
plt.subplot(2,3,1)
plt.pcolormesh(v11[ialt1,:,:])
plt.colorbar()

plt.subplot(2,3,2)
plt.pcolormesh(v12[ialt1,:,:])
plt.colorbar()

plt.subplot(2,3,3)
plt.pcolormesh(dv1[ialt1,:,:])
plt.colorbar()

plt.subplot(2,3,4)
plt.pcolormesh(v11[ialt2,:,:])
plt.colorbar()

plt.subplot(2,3,5)
plt.pcolormesh(v12[ialt2,:,:])
plt.colorbar()

plt.subplot(2,3,6)
plt.pcolormesh(dv1[ialt2,:,:])
plt.colorbar()


##### Density comparison
plt.subplots(2,3,dpi=150)
plt.subplot(2,3,1)
plt.pcolormesh(ne1[ialt1,:,:])
plt.colorbar()

plt.subplot(2,3,2)
plt.pcolormesh(ne2[ialt1,:,:])
plt.colorbar()

plt.subplot(2,3,3)
plt.pcolormesh(dne[ialt1,:,:])
plt.colorbar()

plt.subplot(2,3,4)
plt.pcolormesh(ne1[ialt2,:,:])
plt.colorbar()

plt.subplot(2,3,5)
plt.pcolormesh(ne2[ialt2,:,:])
plt.colorbar()

plt.subplot(2,3,6)
plt.pcolormesh(dne[ialt2,:,:])
plt.colorbar()

