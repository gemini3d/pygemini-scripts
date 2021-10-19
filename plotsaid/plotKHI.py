# imports
import gemini3d.read
import numpy as np
import matplotlib.pyplot as plt
import os

# location of simulation output
direc = "/Users/zettergm/simulations/KHI_periodic_SAID_2side_ell5/"

# set env variables
os.environ["GEMINI_SIMROOT"]="~/simulations/"
plotdir=direc+"/altplots/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

# config and grid data
print("...Loading config and grid...")
cfg = gemini3d.read.config(direc)
xg = gemini3d.read.grid(direc)
x = xg["x2"][2:-2]  # remove ghost cells
y = xg["x3"][2:-2]
z = xg["x1"][2:-2]

# reference altitude
altref = 300e3
ialt = np.argmin(abs(z - altref), axis=0)

# input electric field and drifts
t0 = cfg["time"][0]

# load data from a specified set of time indices
its=range(0,len(cfg["time"]))
for it in its:
    simtime=cfg["time"][it]
    print("Loading:  ",simtime)
    dat=gemini3d.read.frame(direc,simtime)
    ne=np.array(dat["ne"])
    Ti=np.array(dat["Ti"])
    v3=np.array(dat["v3"])
    neplot=ne[ialt,:,:]
    Tiplot=Ti[ialt,:,:]
    v3plot=v3[ialt,:,:]
    xnow=0      # present center position of patch

    plt.subplots(1,2,dpi=150,figsize=(9.5,4))
    
    plt.subplot(1,2,1)
    cmap=plt.get_cmap("coolwarm")
    plt.pcolormesh((x-xnow)/1e3,y/1e3,neplot.transpose(),cmap=cmap)
    plt.xlim(-250,250)
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title(cfg["time"][it].strftime("%H:%M:%S"))
    cbarlab="$n_e$ (m$^{-3}$)"
    cbar=plt.colorbar(label=cbarlab)
    ax=plt.gca()
    ax.set_aspect("equal")
    
    plt.subplot(1,2,2)
    cmap=plt.get_cmap("coolwarm")
    plt.pcolormesh((x-xnow)/1e3,y/1e3,Tiplot.transpose(),cmap=cmap)
    plt.xlim(-250,250)
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title(cfg["time"][it].strftime("%H:%M:%S"))
    cbarlab="$T_i$ (K)"
    cbar=plt.colorbar(label=cbarlab)
    ax=plt.gca()
    ax.set_aspect("equal")       
    
    plt.savefig(plotdir+"/ne"+str(simtime)+"s.png")
    plt.close("all")
