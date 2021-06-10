import gemini3d.read
from gemini3d.grid.tilted_dipole import tilted_dipole3d
import numpy as np
import matplotlib.pyplot as plt

# generate the grid using python
cfg=dict()
cfg["dtheta"]=11
cfg["dphi"]=105
cfg["lp"]=128
cfg["lq"]=256
cfg["lphi"]=128
cfg["altmin"]=80e3
cfg["glat"]=56
cfg["glon"]=0
cfg["gridflag"]=0
cfg["openparm"]=50

xg=tilted_dipole3d(cfg)


# plot the grid
mlon=xg["phi"]*180/np.pi
mlat=90-xg["theta"]*180/np.pi
alt=xg["alt"]

ax = plt.figure(dpi=150).gca(projection='3d')

plt.plot(mlon[0,:,0],mlat[0,:,0],alt[0,:,0]/1e3)
plt.plot(mlon[-1,:,0],mlat[-1,:,0],alt[-1,:,0]/1e3)
plt.plot(mlon[:,0,0],mlat[:,0,0],alt[:,0,0]/1e3)
plt.plot(mlon[:,-1,0],mlat[:,-1,0],alt[:,-1,0]/1e3)

plt.plot(mlon[0,:,-1],mlat[0,:,0],alt[0,:,-1]/1e3)
plt.plot(mlon[-1,:,-1],mlat[-1,:,0],alt[-1,:,-1]/1e3)
plt.plot(mlon[:,0,-1],mlat[:,0,0],alt[:,0,-1]/1e3)
plt.plot(mlon[:,-1,-1],mlat[:,-1,0],alt[:,-1,-1]/1e3)

plt.plot(mlon[0,0,:],mlat[0,0,:],alt[0,0,:]/1e3)
plt.plot(mlon[0,-1,:],mlat[0,-1,:],alt[0,-1,:]/1e3)
plt.plot(mlon[-1,-1,:],mlat[-1,-1,:],alt[-1,-1,:]/1e3)
plt.plot(mlon[-1,0,:],mlat[-1,0,:],alt[-1,0,:]/1e3)

plt.xlabel("mlon")
plt.ylabel("mlat")
ax.set_zlabel("alt")
plt.show(block=False)


