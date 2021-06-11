import numpy as np
from matplotlib.pyplot import figure
import typing as T


def plotoutline2D(xg: dict[str, T.Any]):
    """plot an outline of a 2D grid in mlat and altitude"""

    mlat = np.degrees(90 - xg["theta"])
    alt = xg["alt"]

    fg = figure(dpi=100)
    ax = fg.gca()

    ax.plot(mlat[0, :, 0], alt[0, :, 0] / 1e3)
    ax.plot(mlat[-1, :, 0], alt[-1, :, 0] / 1e3)
    ax.plot(mlat[:, 0, 0], alt[:, 0, 0] / 1e3)
    ax.plot(mlat[:, -1, 0], alt[:, -1, 0] / 1e3)
    ax.set_xlabel("mlat")
    ax.set_ylabel("alt")


def plotoutline3D(xg: dict[str, T.Any]):
    """plot 3D grid outline"""

    mlon = np.degrees(xg["phi"])
    mlat = np.degrees(90 - xg["theta"])
    alt = xg["alt"]

    fg = figure(dpi=150)
    ax = fg.gca(projection="3d")

    ax.plot(mlon[0, :, 0], mlat[0, :, 0], alt[0, :, 0] / 1e3)
    ax.plot(mlon[-1, :, 0], mlat[-1, :, 0], alt[-1, :, 0] / 1e3)
    ax.plot(mlon[:, 0, 0], mlat[:, 0, 0], alt[:, 0, 0] / 1e3)
    ax.plot(mlon[:, -1, 0], mlat[:, -1, 0], alt[:, -1, 0] / 1e3)

    ax.plot(mlon[0, :, -1], mlat[0, :, 0], alt[0, :, -1] / 1e3)
    ax.plot(mlon[-1, :, -1], mlat[-1, :, 0], alt[-1, :, -1] / 1e3)
    ax.plot(mlon[:, 0, -1], mlat[:, 0, 0], alt[:, 0, -1] / 1e3)
    ax.plot(mlon[:, -1, -1], mlat[:, -1, 0], alt[:, -1, -1] / 1e3)

    ax.plot(mlon[0, 0, :], mlat[0, 0, :], alt[0, 0, :] / 1e3)
    ax.plot(mlon[0, -1, :], mlat[0, -1, :], alt[0, -1, :] / 1e3)
    ax.plot(mlon[-1, -1, :], mlat[-1, -1, :], alt[-1, -1, :] / 1e3)
    ax.plot(mlon[-1, 0, :], mlat[-1, 0, :], alt[-1, 0, :] / 1e3)

    ax.set_xlabel("mlon")
    ax.set_ylabel("mlat")
    ax.set_zlabel("alt")
