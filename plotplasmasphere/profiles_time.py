# imports
import numpy as np
import matplotlib.pyplot as plt
import gemini3d.read

# output data from simulation
direc="~/simulations/raid/plasmasphere2D_eq"

# load density from all data frames
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
lx1=xg["x1"].size-4
lx2=xg["x2"].size-4
lx3=xg["x3"].size-4
lt=len(cfg["time"])
netime=np.empty((lx2,lt))
for it in range(0,lt):
    print(cfg["time"][it])
    dat=gemini3d.read.frame(direc,cfg["time"][it])
    z=xg["alt"][lx1//2,:,0]
    netime[:,it]=dat["ne"][lx1//2,:,0]

# identify altitudes of interest
izmin=np.argmin(abs(z-80e3))

# color contour plot
plt.figure(dpi=150)
plt.pcolormesh(cfg["time"],z[izmin:]/1e3,np.log10(netime[izmin:,:]))
cbar=plt.colorbar()
plt.clim(7,12.5)
cbar.set_label=("$log_{10} n_e$ (m$^{-3}$)")
plt.xlabel("UT")
plt.ylabel("z (km)")
plt.show(block=False)
