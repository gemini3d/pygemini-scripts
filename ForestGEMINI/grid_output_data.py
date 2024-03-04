#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 14:44:52 2023

Load a ForestGemini vtu file and interpolate to uniform grid

@author: zettergm
"""


import vtk.vtk

# The source file
file_name = ""

# Read the source file.
reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(file_name)
reader.Update()  # Needed because of GetScalarRange
output = reader.GetOutput()
potential = output.GetPointData().GetArray("potential")