# imports
import gemini3d.read
import os
import numpy as np
import matplotlib.pyplot as plt
from plotGDI_tools import padstr

plt.ioff()    # so matplotlib doesn't take over the entire computer :(
flagquiver=False

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
direc = home+"/simulations/raid2/simulations_GDI_airglow/v5/GDI_airglow_disturb_rot_profile_offset_glow/"
if (flagquiver): 
    plotdir=direc+"/customplots_quiver/"
else:
    plotdir=direc+"/customplots_noquiver/"
    
    
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
Ey = -20e-3
vx = -Ey / Bmag  # prescribed background drift of patch
x0 = -1500e3  # initial patch position
t0 = cfg["time"][0]

# load data from a specified set of time indices
its=range(0,len(cfg["time"]))
#its=range(len(cfg["time"])//4-1,len(cfg["time"])//4)
plt.figure(dpi=150)
for it in its:
    print("Loading:  ",cfg["time"][it])
    dat=gemini3d.read.frame(direc,cfg["time"][it])
    ne=np.array(dat["ne"])
    neplot=ne[ialt,:,:]
    deltat=(cfg["time"][it]-t0).total_seconds()
    xnow=x0+vx*deltat      # present center position of patch
    #xnow=0
    
    v2plot=np.array(dat["v2"])[ialt,:,:]-vx
    v3plot=np.array(dat["v3"])[ialt,:,:]  
    stride=10

    cmap = plt.get_cmap("coolwarm")
    plt.clf();
    #plt.pcolormesh((x - xnow) / 1e3, y / 1e3, neplot.transpose(), cmap=cmap, shading="auto")
    plt.pcolormesh(x / 1e3, y / 1e3, neplot.transpose(), cmap=cmap, shading="auto")
    cbarlab="$n_e$ (m$^{-3}$)"
    plt.clim(0e11,2.5e11)
    cbar=plt.colorbar(label=cbarlab,cmap=cmap)
    if (flagquiver):
#        plt.quiver((x[0:x.size:stride] - xnow) / 1e3, y[0:y.size:stride] / 1e3, 
#                   v2plot.transpose()[0:x.size:stride,0:y.size:stride], 
#                   v3plot.transpose()[0:x.size:stride,0:y.size:stride], color="white")
        X,Y=np.meshgrid(x[0:x.size:stride] / 1e3, y[0:y.size:stride] / 1e3)
        plt.quiver(X,Y, 
                   v2plot.transpose()[0:y.size:stride, 0:x.size:stride], 
                   v3plot.transpose()[0:y.size:stride, 0:x.size:stride], color="white")
#    plt.xlim(-800,800)
#    plt.ylim(-800,800)
    plt.xlim(xnow/1e3-800,xnow/1e3+800)
    plt.ylim(-800,800)
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title(cfg["time"][it].strftime("%H:%M:%S"))
    ax=plt.gca()
    #ax.set_aspect(5)
    #plt.show(block=False)
    simtime=(cfg["time"][it]-cfg["time"][0]).total_seconds()
    simtimestr=str(simtime)
    simtimestr=padstr(simtime,simtimestr)
    plt.savefig(plotdir+"/"+parmlbl+simtimestr+"s_large.png")

