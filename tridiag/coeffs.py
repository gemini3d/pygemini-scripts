#!/usr/bin/env python3
"""
Example code to load the parabolic coefficient data into an ipython workspace

@author: zettergm
"""

from read_coeffs import load_coeffs

filename = "~/4096pts.h5"
t, coeffs, rhs, temperature = load_coeffs(filename)
