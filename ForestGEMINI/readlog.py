#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 15:19:07 2025

@author: zettergm
"""

import re
import numpy as np
import matplotlib.pyplot as plt


###############################################################################
def parse_data(log):
    # Find the number of diagnostic prints
    count=0
    for i in range(0,len(log)):
        imatch=log[i].find('patches:  ')
        if (imatch>=0):
            count=count+1

    # Global number of patches
    magic_patches=np.zeros((count))
    gemini_patches=np.zeros((count))
    count=0
    for i in range(0,len(log)):
        imatch=log[i].find('patches:  ')       
        if (imatch>0):
            npatches = re.findall(r"\d+",log[i])
            magic_patches[count]=int(npatches[0])
            gemini_patches[count]=int(npatches[1])
            count=count+1
            
    # Data exchange time
    figments_time=np.zeros(count)       
    count=0
    for i in range(0,len(log)):
        imatch=log[i].find("Time for figments: ")
        if (imatch>0):
            figtime = re.findall(r"\d+\.\d+",log[i])
            figments_time[count]=float(figtime[0])
            count=count+1

    # Time in simulation
    t_model_magic=np.zeros(count)
    t_model_gemini=np.zeros(count)
    count=0
    for i in range(0,len(log)):
        imatch=log[i].find("Time stepping paused:")
        if (imatch>0):
            simtime = re.findall(r"\d+\.\d+",log[i])
            t_model_gemini[count]=simtime[0]
            t_model_magic[count]=simtime[1]
            count=count+1

    parsed_data=dict()
    parsed_data["magic_patches"]=magic_patches
    parsed_data["gemini_patches"]=gemini_patches
    parsed_data["figments_time"]=figments_time
    parsed_data["t_model_gemini"]=t_model_gemini
    parsed_data["t_model_magic"]=t_model_magic   

    return parsed_data
###############################################################################


###############################################################################
def remove_outliers(p):
    ## We have some outliers from our shitty computer so do some binning to try
    ##        to get a meaningful trend and variance
    threshold=0.2
    
    ##  MAGIC Forest binned exchange data
    _,magic_bins = np.histogram(p["magic_patches"])
    magic_binned_times=[None]*(magic_bins.size-1)
    magic_binned_outliers=[None]*(magic_bins.size-1)
    magic_time = np.zeros(magic_bins.size-1)
    magic_dtime=np.zeros(magic_bins.size-1)
    for i in range(0,magic_bins.size-1):
        inds=np.argwhere(np.logical_and(p["magic_patches"]>magic_bins[i], p["magic_patches"]<magic_bins[i+1]))
        timedata=p["figments_time"][inds]     # create an array of data for this bin
        magic_binned_times[i]=timedata[timedata<threshold]
        magic_binned_outliers[i]==timedata[timedata>=threshold]
        magic_time[i]=magic_binned_times[i].mean()
        magic_dtime[i]=magic_binned_times[i].std()
    magic_bins_ctr=1/2*(magic_bins[0:-1]+magic_bins[1:])
    magic_bins_width=(magic_bins[1:]-magic_bins[0:-1])
    
    ## GEMINI binned exchange data
    _,gemini_bins = np.histogram(p["gemini_patches"])
    gemini_binned_times=[None]*(gemini_bins.size-1)
    gemini_binned_outliers=[None]*(gemini_bins.size-1)
    gemini_time = np.zeros(gemini_bins.size-1)
    gemini_dtime=np.zeros(gemini_bins.size-1)
    for i in range(0,gemini_bins.size-1):
        inds=np.argwhere(np.logical_and(p["gemini_patches"]>gemini_bins[i], p["gemini_patches"]<gemini_bins[i+1]))
        timedata=p["figments_time"][inds]     # create an array of data for this bin
        gemini_binned_times[i]=timedata[timedata<threshold]
        gemini_binned_outliers[i]=timedata[timedata>=threshold]
        gemini_time[i]=gemini_binned_times[i].mean()
        gemini_dtime[i]=gemini_binned_times[i].std()
    gemini_bins_ctr=1/2*(gemini_bins[0:-1]+gemini_bins[1:])
    gemini_bins_width=(gemini_bins[1:]-gemini_bins[0:-1])
    
    binned_data=dict()
    binned_data["magic_bins"]=magic_bins
    binned_data["magic_bins_ctr"]=magic_bins_ctr
    binned_data["magic_bins_width"]=magic_bins_width
    binned_data["magic_time"]=magic_time
    binned_data["magic_dtime"]=magic_dtime
    binned_data["magic_binned_times"]=magic_binned_times
    binned_data["magic_binned_outliers"]=magic_binned_outliers   
    binned_data["gemini_bins"]=gemini_bins
    binned_data["gemini_bins_ctr"]=gemini_bins_ctr
    binned_data["gemini_bins_width"]=gemini_bins_width
    binned_data["gemini_time"]=gemini_time
    binned_data["gemini_dtime"]=gemini_dtime
    binned_data["gemini_binned_times"]=gemini_binned_times
    binned_data["gemini_binned_outliers"]=gemini_binned_outliers    
    
    return binned_data
###############################################################################


###############################################################################
#  Main part of script
###############################################################################

file = open("log.out")
log = file.readlines()
file.close()
pdat = parse_data(log)
bdat=remove_outliers(pdat)


## Plot some synopsis of how the number of patches evolved during run
plt.figure(dpi=150)
plt.plot(pdat["t_model_magic"], pdat["magic_patches"])
plt.plot(pdat["t_model_gemini"], pdat["gemini_patches"])
plt.xlabel("simulation time")
plt.ylabel("number of patches")
plt.legend(("MAGIC Forest","Trees GEMINI"))
plt.show()

# Some statistical summary of exchange times vs. number of patches
plt.figure(dpi=150)
plt.bar(bdat["magic_bins_ctr"],bdat["magic_time"],width=bdat["magic_bins_width"])
plt.errorbar(bdat["magic_bins_ctr"], bdat["magic_time"], yerr=bdat["magic_dtime"],fmt="o",color="k")
plt.xlabel("no. of patches")
plt.ylabel("data exchange time")
plt.title("MAGIC Forest")

plt.figure(dpi=150)
plt.bar(bdat["gemini_bins_ctr"],bdat["gemini_time"],width=bdat["gemini_bins_width"])
plt.errorbar(bdat["gemini_bins_ctr"],bdat["gemini_time"],yerr=bdat["gemini_dtime"],fmt="o",color="k")
plt.xlabel("no. of patches")
plt.ylabel("data exchange time")
plt.title("Trees GEMINI")

# plt.figure(dpi=150)
# plt.bar(bdat["gemini_bins_ctr"],bdat["gemini_binned_times"][:].size,width=bdat["gemini_bins_width"])
# plt.xlabel("no. of patches")
# plt.ylabel("no. of samples in given range")
# plt.title("Trees GEMINI")

# Check distribution of data for some bin
binno=6
plt.figure(dpi=150)
plt.hist(bdat["gemini_binned_times"][binno],bins=20)
plt.title("distribution of exchange times within bin")



# ###### Plot some performance diagnostics
# plt.subplots(1,2,dpi=150)
# plt.subplot(1,2,1)
# #plt.scatter(magic_patches,figments_time)
# #isort=np.argsort(magic_patches)
# #magic_patches=magic_patches[isort]
# #figments_time_magic=figments_time[isort]
# #plt.hist(magic_patches,figments_time_magic)
# plt.ylabel("data exchange time")
# plt.xlabel("no. of MAGIC patches")
# plt.axis( (magic_patches.min(), magic_patches.max(), 0, 0.1) )
# plt.subplot(1,2,2)
# #plt.scatter(gemini_patches,figments_time)
# #isort=np.argsort(gemini_patches)
# #gemini_patches=gemini_patches[isort]
# #figments_time_gemini=figments_time[isort]
# #plt.hist(gemini_patches,figments_time_gemini)
# plt.ylabel("data exchange time")
# plt.xlabel("no. of GEMINI patches")
# plt.axis( (gemini_patches.min(), gemini_patches.max(), 0, 0.1) )
# plt.show()




