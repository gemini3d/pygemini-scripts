# imports
import gemini3d.read
import os
import numpy as np
import matplotlib.pyplot as plt
from plotGDI_tools import padstr


# set some font sizes
SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# location of simulation output
home=os.path.expanduser("~")
direc = home+"/simulations/GDI_round_strong/"
plotdir=direc+"/customplots2/"
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)
parmlbl="ne"

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
Bmag = 50000e-9
Ey = -43.8e-3
vx = -Ey / Bmag  # prescribed background drift of patch
x0 = -180e3  # initial patch position
t0 = cfg["time"][0]

# load data from a specified set of time indices
its=range(0,640,1)
plt.figure(dpi=150)
for it in its:
    print("Loading:  ",cfg["time"][it])
    dat=gemini3d.read.frame(direc,cfg["time"][it])
    ne=np.array(dat["ne"])
    neplot=ne[ialt,:,:]
    deltat=(cfg["time"][it]-t0).total_seconds()
    #xnow=x0+vx*deltat      # present center position of patch
    xnow=0

    #plt.figure(dpi=150)
    cmap = plt.get_cmap("coolwarm")
    plt.clf();
    #cmap = plt.get_cmap("viridis")
    plt.pcolormesh((x - xnow) / 1e3, y / 1e3, neplot.transpose(), cmap=cmap, shading="auto")
    #plt.xlim(-75, 50)
    #plt.xlim(-37.5,37.5)
    plt.xlim(-200,200)
    plt.ylim(-200,200)
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title(cfg["time"][it].strftime("%H:%M:%S"))
#    plt.clim(1e11,5e11)
    plt.clim(0.5e11,2.4e11)
    cbarlab="$n_e$ (m$^{-3}$)"
    cbar=plt.colorbar(label=cbarlab)
    ax=plt.gca()
    #ax.set_aspect(5)
    plt.show(block=False)
    simtime=(cfg["time"][it]-cfg["time"][0]).total_seconds()
    simtimestr=str(simtime)
    simtimestr=padstr(simtime,simtimestr)
    plt.savefig(plotdir+"/"+parmlbl+simtimestr+"s_large.png")
#    plt.figure(dpi=150)
#    #cmap=plt.get_cmap("coolwarm")
#    cmap = plt.get_cmap("viridis")
#    plt.pcolormesh((x-xnow)/1e3,y/1e3,neplot.transpose(),cmap=cmap)
#    plt.xlim(-60,20)
#    plt.ylim(-1,1)
#    plt.xlabel("x (km)")
#    plt.ylabel("y (km)")
#    plt.title(cfg["time"][it].strftime("%H:%M:%S"))
#    plt.clim(1e11,3.7e11)
#    cbarlab="$n_e$ (m$^{-3}$)"
#    cbar=plt.colorbar(label=cbarlab)
#    #ax=plt.gca()
#    #ax.set_aspect("equal")
#    plt.show(block=False)
#    simtime=(cfg["time"][it]-cfg["time"][0]).total_seconds()
#    plt.savefig(plotdir+"/"+parmlbl+str(simtime)+"s_small.png")
