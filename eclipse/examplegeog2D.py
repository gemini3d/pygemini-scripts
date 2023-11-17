#!/usr/bin/env python3
"""
@author: zettergm
"""

import gemini3d.read
from plotcurv import plotcurv2D
import matplotlib.pyplot as plt
from gemini3d.grid.gridmodeldata import model2magcoords,model2geogcoords
import numpy as np

# load some sample data (2D)
#direc = "~/simulations/raid/EIAnowinds/"
it=129    #lazy
direc = "~/simulations/raid2/simulations_eclipse/Oct2023_eclipse_solmax_control/"
direc2 = "~/simulations/raid2/simulations_eclipse/Oct2023_eclipse_solmax/"
direc3 = "~/simulations/raid2/simulations_eclipse/Oct2023_eclipse_solmin_control/"
direc4 = "~/simulations/raid2/simulations_eclipse/Oct2023_eclipse_solmin/"
cfg = gemini3d.read.config(direc)
print("Time frame for comparison:  ",cfg["time"][86])
xg = gemini3d.read.grid(direc)
dat = gemini3d.read.frame(direc, cfg["time"][it])
dat2 = gemini3d.read.frame(direc2, cfg["time"][it])
cfg3=gemini3d.read.config(direc3)
dat3 = gemini3d.read.frame(direc3, cfg3["time"][it])
dat4 = gemini3d.read.frame(direc4, cfg3["time"][it])


# grid data
lalt = 1024
llat = 1024
llon = 1
parm = dat["ne"]
parm2 = dat2["ne"]
parm3 = dat3["ne"]
parm4 = dat4["ne"]
alti, gloni, glati, parmgeoi = model2geogcoords(xg, parm, lalt, llon, llat)
alti, gloni, glati, parm2geoi = model2geogcoords(xg, parm2, lalt, llon, llat)
alti, gloni, glati, parm3geoi = model2geogcoords(xg, parm3, lalt, llon, llat)
alti, gloni, glati, parm4geoi = model2geogcoords(xg, parm4, lalt, llon, llat)


# plot data with pygemini standard output
#plotcurv2D(xg, dat["ne"], lalt=1024, llat=1024)
#plt.show(block=False)

# now plot interpolated data
plt.subplots(4,1,dpi=150,figsize=(8,10))

plt.subplot(4,1,1)
plt.pcolormesh(glati,alti/1e3,parmgeoi.reshape((lalt,llat)),shading="interp")
plt.ylim((0,750))
plt.colorbar(label="$n_e$ prior (sol. max)")
plt.ylabel("altitude (km)")
#plt.xlabel("geog. lat.")

plt.subplot(4,1,2)
plt.pcolormesh(glati,alti/1e3,parm2geoi.reshape((lalt,llat)),shading="interp")
plt.ylim((0,750))
plt.colorbar(label="$n_e$ annularity (sol. max)")
plt.ylabel("altitude (km)")
#plt.xlabel("mag. lat.")

plt.subplot(4,1,3)
plt.pcolormesh(glati,alti/1e3,parm3geoi.reshape((lalt,llat)),shading="interp")
plt.ylim((0,750))
plt.colorbar(label="$n_e$ prior (sol. min)")
plt.ylabel("altitude (km)")
plt.xlabel("geog. lat.")

plt.subplot(4,1,4)
plt.pcolormesh(glati,alti/1e3,parm4geoi.reshape((lalt,llat)),shading="interp")
plt.ylim((0,750))
plt.colorbar(label="$n_e$ annularity (sol. min)")
plt.ylabel("altitude (km)")
plt.xlabel("geog. lat.")

# plt.subplot(3,1,3)
# plt.pcolormesh(glati,alti/1e3,(parm2geoi-parmgeoi).reshape((lalt,llat)),shading="interp")
# plt.ylim((0,750))
# plt.colorbar(label="$n_e$")
# plt.ylabel("altitude (km)")
# plt.xlabel("geog. lat.")

plt.savefig("meriodinal_slice.png")


# extract a meaningful profile for the experiment
ecglat=33.0
ilat=np.argmin(abs(glati-ecglat))

plt.figure(dpi=150)
plt.plot(np.log10(parmgeoi[:,:,ilat]),alti/1e3)
plt.plot(np.log10(parm2geoi[:,:,ilat]),alti/1e3)
plt.plot(np.log10(parm3geoi[:,:,ilat]),alti/1e3)
plt.plot(np.log10(parm4geoi[:,:,ilat]),alti/1e3)
plt.legend(["Prior to eclipse (sol. max)","Annularity (sol. max)",
            "Prior to eclipse (sol. min)","Annularity (sol. min)"])
plt.xlim((9, 12.7))
plt.ylim((0, 750))
plt.xlabel("log$_{10}$ plasma density")
plt.ylabel("altitude")

plt.savefig("alt_profiles.png")


# latitude profile of density

altref=500e3    #LLITED orbital altitude
ialt=np.argmin(abs(alti-altref))

plt.figure(dpi=150)
plt.plot(glati,np.log10(parmgeoi[ialt,:,:]).transpose())
plt.plot(glati,np.log10(parm2geoi[ialt,:,:]).transpose())
plt.plot(glati,np.log10(parm3geoi[ialt,:,:]).transpose())
plt.plot(glati,np.log10(parm4geoi[ialt,:,:]).transpose())
plt.legend(["Prior to eclipse (sol. max)","Annularity (sol. max)",
            "Prior to eclipse (sol. min)","Annularity (sol. min)"])
#plt.xlim((9, 12.7))
#plt.ylim((0, 750))
plt.ylabel("log$_{10}$ plasma density")
plt.xlabel("geog. lat.")

plt.savefig("lat_profiles.png")



