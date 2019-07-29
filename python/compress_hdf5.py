#!/usr/bin/env python3
#
# This script tests the effect of the scale parameter in HDF5 image
# compression. It writes uncompressed and compressed versions of the
# images as HDF5 files using the h5py package. The compressed files
# are read in again to compute the RMS errors.
#
# The results are written as a table in Confluence wiki markup, so it
# can be cut and pasted into the page with just a little light
# formatting by hand afterwards.

from common import *
import os
import numpy as np
import h5py

iform = '{p}/{d}/{d}.fits'
oform = '{p}/{d}/{d}.hdf5'

nssteps = 3
chunksize = 1024

# Table header

table = []
table.append('|| Name || First scale value || || || Second scale value || || || Third scale value || || ||')
table.append('|| ||' + ' s || Size || RMS ||' * nssteps)

# Loop over datasets.

for d in datasets:

    ifile = iform.format(p=dat_dir, d=d)
    ofile = oform.format(p=dat_dir, d=d)
    
    # Read original image from FITS file.

    _, image_orig = read_image(ifile, squeeze=False)

    # Set chunk size

    chunks = list(image_orig.shape)
    if chunks[-1] > chunksize:
        chunks[-1] = chunksize
    if chunks[-2] > chunksize:
        chunks[-2] = chunksize
    chunks = tuple(chunks)

    # Write uncompressed image.

    with h5py.File(ofile, 'w') as f:
        dset = f.create_dataset('image', image_orig.shape, chunks=chunks)
        dset[...] = image_orig

    # Get size of uncompressed image file.

    size_orig = os.path.getsize(ofile)

    # Remove uncompressed image file.

    os.remove(ofile)

    # Estimate noise sigma using median absolute deviation.

    med = np.median(image_orig)
    mad = np.median(np.abs(image_orig - med))
    sigma = 1.4826 * mad

    # Get starting s value from sigma.

    s_start = - int(np.floor(np.log10(sigma)))

    row = '| {} |'.format(d)

    # Loop over s values.

    for s in range(s_start, s_start + nssteps):

        print('Compressing {} with s value {}'.format(d, s))

        # Write compressed image.

        with h5py.File(ofile, 'w') as f:
            dset = f.create_dataset('image', image_orig.shape,
                                    chunks=chunks, scaleoffset=s,
                                    compression='gzip',
                                    compression_opts=5)
            dset[...] = image_orig

        # Get size of compressed image file.

        size_comp = os.path.getsize(ofile)

        # Read compressed image file.

        with h5py.File(ofile, 'r') as f:
            image_comp = f['image'][...]

        # Remove compressed image file.

        os.remove(ofile)

        rms = np.sqrt(np.mean((image_comp - image_orig)**2))
        
        print('-> compression factor', size_comp/size_orig, 'rms', rms)
        row += ' {} | {:.3f} | {} |'.format(s, size_comp/size_orig, pp(rms)) 

    table.append(row)

# Write table of results.

rfile = '{p}/table_hdf5.txt'.format(p=res_dir)

print('Writing results to', rfile)

with open(rfile, 'w') as f:
    for row in table:
        f.write(row + '\n')
