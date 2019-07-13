#!/usr/bin/env python3

from common import *
import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import astropy.io.fits as fits

iform = '{p}/{d}/{d}_2d.fits'
oform = '{p}/image_{d}.png'

cmap = 'cubehelix'
        
for d in datasets:

    print(d)

    ifile = iform.format(p=dat_dir, d=d)
    ofile = oform.format(p=res_dir, d=d)

    with fits.open(ifile) as f:
        npix = f[0].data.shape[-1]
        # If larger than 2048 pixels, read just the central region of
        # the image.
        if npix > 2048:
            centre = npix // 2
            s = slice(centre-1024, centre+1024)
            image = f[0].data[..., s, s]
        else:
            image = f[0].data

    # Find mean and standard deviation of image (iterate once to
    # exclude bright sources).

    mean = np.mean(image)
    rms = np.std(image)
    k = np.abs(image-mean) <= 5.0 * rms
    mean = np.mean(image[k])
    rms = np.std(image[k])

    # Apply tanh normalisation.

    image_plot = np.tanh((image - mean) / (10.0 * rms))

    plt.figure()
    plt.title(d)
    plt.imshow(image_plot, cmap=cmap)
    plt.colorbar()
    plt.savefig(ofile, dpi=250)
