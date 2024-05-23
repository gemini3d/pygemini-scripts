#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 17:21:48 2024

@author: zettergm
"""

import h5py

direc="/Users/zettergm/simulations/ssd/isinglass_78_lowres/inputs/fields/"
filename=direc+"simsize.h5"
outname=direc+"simsize2.h5"
f=h5py.File(filename,"r")
f.close()

llon=128; llat=512;
f = h5py.File(outname,"w")
f.create_dataset("/llon",data=llon)
f.create_dataset("/llat",data=llat)
f.close()
