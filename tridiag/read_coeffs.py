#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 18:24:38 2021

illustrates handling of output coefficient file from geminis parabolic solver.  This
takes the output of the test_diffusion1D.f90 program and converts it to numpy arrays

@author: zettergm
"""

# imports
import numpy as np
import h5py


def load_coeffs(filename):
    h5file=h5py.File(filename,"r")
    keylist=list(h5file.keys())
    lx=h5file[keylist[0]].size
    
    # initial cycle through the variables to see how many time steps were output
    indt=0
    for key in keylist:
        if key[0:6]=="coeffs":
            indt=indt+1
    
    # now read time,coefficient, and rhs variables; must convert to numpy arrays in the process
    t=np.zeros(indt)
    coeffs=np.zeros((3,lx,indt))
    rhs=np.zeros((lx,indt))
    temperature=np.zeros((lx,indt))
    indt=0
    for key in keylist:
        if key[0:6]=="coeffs":
            indt=int(key[6:])-1
            coeffs[:,:,indt]=np.array(h5file[key])
        elif key[0:1]=="t":
            indt=int(key[1:])-1
            t[indt]=np.array(h5file[key])
        elif key[0:3]=="rhs":
            indt=int(key[3:])-1
            rhs[:,indt]=np.array(h5file[key])
        elif key[0:7]=="TsEuler":
            indt=int(key[7:])-1
            temperature[:,indt]=np.array(h5file[key])
            
    return [t,coeffs,rhs,temperature]