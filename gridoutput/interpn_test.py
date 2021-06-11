#!/usr/bin/env python3
"""
@author: zettergm
"""

import numpy as np
import scipy.interpolate
from matplotlib.pyplot import figure, show

x1 = np.linspace(-1, 1, 384)
x2 = np.linspace(-1, 1, 96)
x3 = np.linspace(-1, 1, 64)

X1, X2, X3 = np.meshgrid(x1, x2, x3, indexing="ij")
values = np.sqrt(X1 ** 2 + X2 ** 2 + X3 ** 2)
x1i = np.linspace(-1.1, 1.1, 256)
x2i = np.linspace(-1.1, 1.1, 256)
x3i = np.linspace(-1.1, 1.1, 256)
# x1i=np.random.randn(256)
# x2i=np.random.randn(256)
# x3i=np.random.randn(256)

X1i, X2i, X3i = np.meshgrid(x1i, x2i, x3i, indexing="ij")
xi = np.array((X1i.ravel(), X2i.ravel(), X3i.ravel())).transpose()
valuesi = scipy.interpolate.interpn(
    (x1, x2, x3), values, xi, method="linear", bounds_error=False, fill_value=np.NaN
)
valuesi = valuesi.reshape(256, 256, 256)

fg = figure()
axs = fg.subplots(1, 2)
ax = axs[0]
h = ax.pcolormesh(x1, x2, values[:, :, 32].transpose(), shading="nearest")
fg.colorbar(h, ax=ax)

ax = axs[1]
ax.pcolormesh(x1i, x2i, valuesi[:, :, 128].transpose(), shading="nearest")
fg.colorbar(h, ax=ax)

show()
