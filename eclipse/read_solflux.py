#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:22:07 2024

@author: zettergm
"""

import scipy.io
import matplotlib.pyplot as plt
import numpy as np

# FISM? data input
fname="/Users/zettergm/data/solar_flux/fism_masked_20231014_194000_gitm.sav"
f = scipy.io.readsav(fname)
glat=f["lat"]
glon=f["lon"]
Iinf=f["msk_irradiance_gitm"]
lambda1=f["start_wv"]
lambda2=f["end_wv"]
lambdai=1/2*(lambda1+lambda2)

###############################################################################
plt.figure(dpi=150)
plt.pcolormesh(glon,glat,Iinf[10,:,:].transpose((1,0)),shading="nearest")
plt.show()
plt.xlabel("glon (deg.)")
plt.ylabel("glat (deg.)")
plt.colorbar()
plt.title("Solar Flux")
###############################################################################
# Organizing data -- since eventually we want a 3D mask probably we can have
#   each wavelength bin as its own 'dataset', e.g. we have N+2 datasets where N
#   is the number of wavelength bins (need extra 2 bins for wavelength ranges?)
###############################################################################

# GEMINI wavelength bin limits
lambda1g=np.array([0.05, 0.4, 0.8, 1.8, 3.2, 7.0, 15.5, 22.4, 29.0, 32.0, 54.0, 65.0, 65.0, 
        79.8, 79.8, 79.8, 91.3, 91.3, 91.3, 97.5, 98.7, 102.7])*1e-9
lambda2g=np.array([0.4, 0.8, 1.8, 3.2, 7.0, 15.5, 22.4, 29.0, 32.0, 54.0, 65.0, 79.8, 79.8, 
         91.3, 91.3, 91.3, 97.5, 97.5, 97.5, 98.7, 102.7, 105.0])*1e-9
lambdagi=1/2*(lambda1g+lambda2g)  # center of wavelength bin

