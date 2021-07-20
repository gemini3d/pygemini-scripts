# imports
import numpy as np
import matplotlib.pyplot as plt
import gemini3d.read

# output data from simulation
direc="~/simulations/plasmasphere2D_eq"

# load the last data frame
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)

# daytime conditions
dat=gemini3d.read.frame(direc,cfg["time"][-1])

# take an altitude slice
lx1,lx2,lx3=dat["ne"].shape
z=xg["alt"][lx1//2,:,0]
ne=dat["ne"][lx1//2,:,0]

# nighttime
dat=gemini3d.read.frame(direc,cfg["time"][-13])
ne2=dat["ne"][lx1//2,:,0]


# plot
plt.figure(dpi=150)
plt.loglog(ne,z/1e3)
plt.loglog(ne2,z/1e3)
plt.xlabel("$n_e$ (m$^{-3}$)")
plt.xlim(1e7,5e12)
plt.ylabel("z (km)")
plt.ylim([150,30000])
plt.show(block=False)
