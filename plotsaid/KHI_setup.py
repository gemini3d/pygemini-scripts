#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 09:42:56 2021

@author: zettergm
"""

import numpy as np
import matplotlib.pyplot as plt

x2=np.linspace(-200e3,200e3,256)

n0=3e11
R=5
v0=2000
gap=50e3
ell=10e3
delta=100

vn=-v0*(1+R)/(1-R)
# if vn>0:
#     vn+=delta
# else:
#     vn-=delta
v=v0 * (np.tanh((x2-gap) /ell) - np.tanh((x2+gap)/ell) + 1)
n= (n0* (v0 - vn) / (v - vn) )
v-=vn

plt.subplots(1,3)

plt.subplot(1,3,1)
plt.plot(x2,v)

plt.subplot(1,3,2)
plt.plot(x2,v+vn)

plt.subplot(1,3,3)
plt.plot(x2,n)
plt.show(block=False)
