from gemini3d.grid.tilted_dipole import tilted_dipole3d
from plotgrid import plotoutline3D,plotoutline2D

# generate a 3D grid
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

# plot the 3D grid outline
plotoutline3D(xg)

# generate a 2D grid
cfg=dict()
cfg["dtheta"]=11
cfg["dphi"]=105
cfg["lp"]=128
cfg["lq"]=256
cfg["lphi"]=1
cfg["altmin"]=80e3
cfg["glat"]=56
cfg["glon"]=0
cfg["gridflag"]=0
cfg["openparm"]=50
xg=tilted_dipole3d(cfg)

# plot the 2D grid
plotoutline2D(xg)
