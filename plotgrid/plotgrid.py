import gemini3d.read
import numpy as np
import matplotlib.pyplot as plt

xg=gemini3d.read.grid("~/simulations/raid/plasmasphere2D_eq/")

mlat=90-xg["theta"]*180/np.pi
alt=xg["alt"]

plt.figure(dpi=100)
plt.plot(mlat[0,:,0],alt[0,:,0]/1e3)
plt.plot(mlat[-1,:,0],alt[-1,:,0]/1e3)
plt.plot(mlat[:,0,0],alt[:,0,0]/1e3)
plt.plot(mlat[:,-1,0],alt[:,-1,0]/1e3)
plt.xlabel("mlat")
plt.ylabel("alt")
plt.show()


