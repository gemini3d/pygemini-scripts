#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:23:02 2024

@author: zettergm
"""

import h5py
import matplotlib.pyplot as plt
import numpy
import os

# matplotlib settings
plt.ioff()    # so matplotlib doesn't take over the entire computer :(
SMALL_SIZE = 6
MEDIUM_SIZE = 8
BIGGER_SIZE = 10
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# locations for everything
basedir="/Users/zettergm/simulations/ssd/QPR_0424/half.vs.full/"
direc1="full_gemini_output_hdf5/"
direc2="half_gemini_output_hdf5/"
filenames=["fort_frame_0016.vtu.hdf5", "fort_frame_0017.vtu.hdf5", "fort_frame_0018.vtu.hdf5", 
           "fort_frame_0019.vtu.hdf5", "fort_frame_0020.vtu.hdf5"]
plotdir=basedir+"plots/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

# iterate of gridded data that we want to compare, make plots, and save to disk
plt.subplots(2,3,dpi=200)
for fname in filenames:  
    f1=h5py.File(basedir+direc1+fname, "r")
    f2=h5py.File(basedir+direc2+fname, "r")

    parmlbls=f1["parmlbls"][:]
    parmsi=f1["parmi"][:]
    v11=parmsi[:,:,:,1]
    #ne1=parmsi[:,:,:,0]
    z=f1["x1i"][:]
    x=f1["x2i"][:]
    y=f1["x3i"][:]
    
    parmlbls=f2["parmlbls"][:]
    parmsi=f2["parmi"][:]
    v12=parmsi[:,:,:,1]
    #ne2=parmsi[:,:,:,0]
    
    dv1=v12-v11
    #dne=ne2-ne1
    
    ialt1=numpy.argmin(abs(z-150e3))
    ialt2=numpy.argmin(abs(z-200e3))
        
    ##### Velocity comparison
    plt.clf()
    plt.subplot(2,2,1)
    plt.pcolormesh(x,y,v11[ialt1,:,:])
    plt.ylabel("mag. lat.")
    plt.title("$v_1$ (m/s)")
    plt.colorbar()
    
    plt.subplot(2,2,2)
    plt.pcolormesh(x,y,v12[ialt1,:,:])
    plt.title("$v_1$ (m/s)")
    plt.colorbar()
    
    # plt.subplot(2,3,3)
    # plt.pcolormesh(x,y,dv1[ialt1,:,:])
    # plt.xlabel("mag. lon.")
    # plt.ylabel("mag. lat.")
    # plt.title("$v_1$")
    # plt.colorbar()
    
    plt.subplot(2,2,3)
    plt.pcolormesh(x,y,v11[ialt2,:,:])
    plt.xlabel("mag. lon.")
    plt.ylabel("mag. lat.")
    plt.colorbar()
    
    plt.subplot(2,2,4)
    plt.pcolormesh(x,y,v12[ialt2,:,:])
    plt.xlabel("mag. lon.")
    plt.colorbar()
    plt.savefig(plotdir+fname+".png")
    
    # plt.subplot(2,3,6)
    # plt.pcolormesh(x,y,dv1[ialt2,:,:])
    # plt.xlabel("mag. lon.")
    # plt.title("$v_1$")
    # plt.colorbar()
    # plt.savefig(plotdir+fname+".png")
