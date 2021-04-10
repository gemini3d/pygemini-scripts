#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 12:46:10 2021

Example code to load the parabolic coefficient data into an ipython workspace

@author: zettergm
"""

from read_coeffs import load_coeffs

filename="/Users/zettergm/Projects/gemini3d/build/src/numerical/diffusion/test_diffusion1d.h5"
[t,coeffs,rhs,temperature]=load_coeffs(filename)
