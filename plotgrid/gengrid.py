from gemini3d.grid.tilted_dipole import tilted_dipole3d
from plotgrid import plotoutline3D, plotoutline2D
from matplotlib.pyplot import show


# %% generate a 3D grid
cfg = {
    "dtheta": 11,
    "dphi": 105,
    "lp": 128,
    "lq": 256,
    "lphi": 128,
    "altmin": 80e3,
    "glat": 56,
    "glon": 0,
    "gridflag": 0,
    "openparm": 50,
}
xg = tilted_dipole3d(cfg)

# %% plot the 3D grid outline
plotoutline3D(xg)

# %% generate a 2D grid
cfg = {
    "dtheta": 11,
    "dphi": 105,
    "lp": 128,
    "lq": 256,
    "lphi": 1,
    "altmin": 80e3,
    "glat": 56,
    "glon": 0,
    "gridflag": 0,
    "openparm": 50,
}
xg = tilted_dipole3d(cfg)

# %% plot the 2D grid
plotoutline2D(xg)

show()
