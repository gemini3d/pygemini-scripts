#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 18:24:38 2021

illustrates handling of output coefficient file from geminis parabolic solver.  This
takes the output of the test_diffusion1D.f90 program and converts it to numpy arrays

@author: zettergm
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import h5py


def load_coeffs(fn) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    fn = Path(fn).expanduser()

    with h5py.File(fn, "r") as f:
        keylist = list(f.keys())
        lx = f[keylist[0]].size

        # initial cycle through the variables to see how many time steps were output
        indt = 0
        for key in keylist:
            if key.startswith("coeffs"):
                indt = indt + 1

        # now read time,coefficient, and rhs variables
        t = np.zeros(indt)
        coeffs = np.zeros((3, lx, indt))
        rhs = np.zeros((lx, indt))
        temperature = np.zeros((lx, indt))
        indt = 0
        for key in keylist:
            if key.startswith("coeffs"):
                indt = int(key[6:]) - 1
                coeffs[:, :, indt] = f[key][:]
            elif key.startswith("t"):
                indt = int(key[1:]) - 1
                t[indt] = np.array(f[key])
            elif key.startswith("rhs"):
                indt = int(key[3:]) - 1
                rhs[:, indt] = f[key][:]
            elif key.startswith("TsEuler"):
                indt = int(key[7:]) - 1
                temperature[:, indt] = f[key][:]

    return t, coeffs, rhs, temperature
