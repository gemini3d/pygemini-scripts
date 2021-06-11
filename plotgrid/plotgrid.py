import numpy as np
import matplotlib.pyplot as plt


def plotoutline2D(xg):
    """plot an outline of a 2D grid in mlat and altitude"""

    mlat = 90 - xg["theta"] * 180 / np.pi
    alt = xg["alt"]

    plt.figure(dpi=100)
    plt.plot(mlat[0, :, 0], alt[0, :, 0] / 1e3)
    plt.plot(mlat[-1, :, 0], alt[-1, :, 0] / 1e3)
    plt.plot(mlat[:, 0, 0], alt[:, 0, 0] / 1e3)
    plt.plot(mlat[:, -1, 0], alt[:, -1, 0] / 1e3)
    plt.xlabel("mlat")
    plt.ylabel("alt")
    plt.show(block=False)


# plot 3D grid outline
def plotoutline3D(xg):
    mlon = xg["phi"] * 180 / np.pi
    mlat = 90 - xg["theta"] * 180 / np.pi
    alt = xg["alt"]

    ax = plt.figure(dpi=150).gca(projection="3d")

    plt.plot(mlon[0, :, 0], mlat[0, :, 0], alt[0, :, 0] / 1e3)
    plt.plot(mlon[-1, :, 0], mlat[-1, :, 0], alt[-1, :, 0] / 1e3)
    plt.plot(mlon[:, 0, 0], mlat[:, 0, 0], alt[:, 0, 0] / 1e3)
    plt.plot(mlon[:, -1, 0], mlat[:, -1, 0], alt[:, -1, 0] / 1e3)

    plt.plot(mlon[0, :, -1], mlat[0, :, 0], alt[0, :, -1] / 1e3)
    plt.plot(mlon[-1, :, -1], mlat[-1, :, 0], alt[-1, :, -1] / 1e3)
    plt.plot(mlon[:, 0, -1], mlat[:, 0, 0], alt[:, 0, -1] / 1e3)
    plt.plot(mlon[:, -1, -1], mlat[:, -1, 0], alt[:, -1, -1] / 1e3)

    plt.plot(mlon[0, 0, :], mlat[0, 0, :], alt[0, 0, :] / 1e3)
    plt.plot(mlon[0, -1, :], mlat[0, -1, :], alt[0, -1, :] / 1e3)
    plt.plot(mlon[-1, -1, :], mlat[-1, -1, :], alt[-1, -1, :] / 1e3)
    plt.plot(mlon[-1, 0, :], mlat[-1, 0, :], alt[-1, 0, :] / 1e3)

    plt.xlabel("mlon")
    plt.ylabel("mlat")
    ax.set_zlabel("alt")
    plt.show(block=False)
