#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:28:55 2024

@author: zettergm
"""

import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import os
import h5py
import datetime
import gemini3d.utils

# GEMINI wavelength bin limits
lambda1g=np.array([0.05, 0.4, 0.8, 1.8, 3.2, 7.0, 15.5, 22.4, 29.0, 32.0, 54.0, 65.0, 65.0, 
        79.8, 79.8, 79.8, 91.3, 91.3, 91.3, 97.5, 98.7, 102.7])*1e-9
lambda2g=np.array([0.4, 0.8, 1.8, 3.2, 7.0, 15.5, 22.4, 29.0, 32.0, 54.0, 65.0, 79.8, 79.8, 
         91.3, 91.3, 91.3, 97.5, 97.5, 97.5, 98.7, 102.7, 105.0])*1e-9
lambdai=1/2*(lambda1g+lambda2g)  # center of GEMINI wavelength bin

# source and target directories
direc="/Volumes/uSDcard1TB/data/solflux/"
outdirec="/Volumes/uSDcard1TB/data/solflux_h5/"
if not os.path.isdir(outdirec):
    os.mkdir(outdirec)
filelist=os.listdir(direc)
filelist.sort()
filelist=filelist[1:]     # get rid of mac OS file


# make a simsize and simgrid file for solar fluxes
f = scipy.io.readsav(direc+filelist[0])
glat=f["lat"]
glon=f["lon"]
f = h5py.File(outdirec+"simsize.h5","w")
f.create_dataset("/llat",data=glat.size)
f.create_dataset("/llon",data=glon.size)
f.close()
f = h5py.File(outdirec+"simgrid.h5","w")
f.create_dataset("/mlat",data=glat)    # mangling glat vs. mlat...
f.create_dataset("/mlon",data=glon)
f.close()


# iterate over input files
for filename in filelist:
    # read data
    fname=direc+filename
    print(fname)
    f = scipy.io.readsav(fname)
    glat=f["lat"]
    glon=f["lon"]
    Iinf=f["msk_irradiance_gitm"]
    lambda1=f["start_wv"]
    lambda2=f["end_wv"]
    lambdactr=1/2*(lambda1+lambda2)*1e-9    # center of wavelength bin, convert nm to m   
    
    Iinfi=np.empty((lambdai.size,glon.size,glat.size))
    for ilat in range(0,glat.size):
        for ilon in range(0,glon.size):
            Iinfi[:,ilon,ilat]=np.interp(lambdai,lambdactr,Iinf[:,ilon,ilat])
    
    # write data in hdf5 format familiar to GEMINI
    ymd=filename[12:20]
    year=ymd[0:4]
    month=ymd[4:6]
    day=ymd[6:]
    hours=filename[21:23]
    minutes=filename[23:25]
    seconds=filename[25:27]
    outdate=datetime.datetime(int(year),int(month),int(day),int(hours),
                              int(minutes),int(seconds))
    outname=gemini3d.utils.datetime2stem(outdate)
    
    f = h5py.File(outdirec+outname+".h5","w")
    f.create_dataset("/Iinf",data=Iinf)
    f.close()