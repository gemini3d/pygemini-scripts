#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 16:47:57 2021

@author: zettergm
"""

import numpy as np
import scipy.interpolate

x1=np.linspace(-1,1,384)
x2=np.linspace(-1,1,96)
x3=np.linspace(-1,1,64)

[X1,X2,X3]=np.meshgrid(x1,x2,x3,indexing="ij")
values=np.sqrt(X1**2+X2**2+X3**2)
#x1i=np.linspace(-1.1,1.1,256)
#x2i=np.linspace(-1.1,1.1,256)
#x3i=np.linspace(-1.1,1.1,256)
x1i=np.random.randn(256)
x2i=np.random.randn(256)
x3i=np.random.randn(256)


[X1i,X2i,X3i]=np.meshgrid(x1i,x2i,x3i,indexing="ij")
xi=np.array((X1i.flatten(),X2i.flatten(),X3i.flatten())).transpose()
valuesi=scipy.interpolate.interpn((x1,x2,x3),values,xi,method="linear",bounds_error=False,fill_value=np.NaN)
valuesi=np.reshape(valuesi,[256,256,256])