#!/usr/bin/env python3
#
# This script rewrites the image files as 2-dimensional FITS images
# (most have 4 dimensions).

from common import *
import astropy.io.fits as fits

iform = '{p}/{d}/{d}.fits'
oform = '{p}/{d}/{d}_2d.fits'

for d in datasets:

    print('Dataset', d)

    ifile = iform.format(p=dat_dir, d=d)
    ofile = oform.format(p=dat_dir, d=d)

    # Read original file.

    with fits.open(ifile) as f:
        image = f[0].data

    # Remove unwanted dimensions.

    image = image.squeeze()

    # Write new file.

    hdu = fits.PrimaryHDU(image)
    hdu.writeto(ofile)
