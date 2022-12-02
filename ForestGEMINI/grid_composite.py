#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 08:51:15 2022

@author: zettergm
"""

import h5py
import gemini3d.grid.tilted_dipole
from gemini3d.hdf5 import write as h5write
import numpy as np

direc="/Users/zettergm/simulations/tohoku20113D_lowres_axineu_fclaw_dneu_refinetest/"

# grab amrgrid composite x1,2,3 coords
hf=h5py.File(direc+"/composite/amrgrid.h5","r")
tmp=hf["x1"][:]
x1=np.empty(tmp.size+4)
x1[2:-2]=tmp
dx1=x1[3]-x1[2]
x1[0:2]=(x1[2]-2*dx1,x1[2]-dx1)
x1[-2:]=(x1[-3]+dx1,x1[-3]+2*dx1)

tmp=hf["x2"][:]
x2=np.empty(tmp.size+4)
x2[2:-2]=tmp
dx2=x2[3]-x2[2]
x2[0:2]=(x2[2]-2*dx2,x2[2]-dx2)
x2[-2:]=(x2[-3]+dx2,x2[-3]+2*dx2)

tmp=hf["x3"][:]
x3=np.empty(tmp.size+4)
x3[2:-2]=tmp
dx3=x3[3]-x3[2]
x3[0:2]=(x3[2]-2*dx3,x3[2]-dx3)
x3[-2:]=(x3[-3]+dx3,x3[-3]+2*dx3)

hf.close()

# regen full grid data from composite coords
xg=gemini3d.grid.tilted_dipole.generate_tilted_dipole3d(x1,x2,x3)

# write the grid to a composite grid file
indat_size=direc+"/composite/simsize.h5"
indat_grid=direc+"/composite/simgrid.h5"
h5write.grid(indat_size, indat_grid, xg)
