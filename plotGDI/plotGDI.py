# imports
import gemini3d.read
import numpy as np
import matplotlib.pyplot as plt

# location of simulation output
direc="~/simulations/raid/GDI_periodic_LL_highres_convertedv2/"

# config and grid data
print("...Loading config and grid...")
cfg=gemini3d.read.config(direc)
xg=gemini3d.read.grid(direc)
x=xg["x2"][2:-2]    # remove ghost cells
y=xg["x3"][2:-2]
z=xg["x1"][2:-2]

# reference altitude
altref=300e3
ialt=np.argmin(abs(z-altref),axis=0)

# input electric field and drifts
Bmag=50000e-9
Ey=-43.8e-3
vx=-Ey/Bmag       # prescribed background drift of patch
x0=-180e3         # initial patch position
t0=cfg["time"][0]

# load data from a specified set of time indices
its=[0,200,400]
for it in its:
    print("Loading:  ",cfg["time"][it])
    dat=gemini3d.read.frame(direc,cfg["time"][it])
    ne=np.array(dat["ne"])
    neplot=ne[ialt,:,:]
    deltat=(cfg["time"][it]-t0).total_seconds()
    xnow=x0+vx*deltat      # present center position of patch
    plt.figure(dpi=150)
    cmap=plt.get_cmap("coolwarm")
    plt.pcolormesh((x-xnow)/1e3,y/1e3,neplot.transpose(),cmap=cmap)
    plt.xlim(-75,75)
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    cbarlab="$n_e$ (m$^{-3}$)"
    cbar=plt.colorbar(label=cbarlab)
    plt.show(block=False)
