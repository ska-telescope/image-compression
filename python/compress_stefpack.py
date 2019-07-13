#!/usr/bin/env python3
#
# This script runs stefpack on the images.  Actually doing the
# compression is *very* slow, but fortunately the size of the
# compressed file can be calculated from the quantised image.
#
# The results are written as a table in Confluence wiki markup, so it
# can be cut and pasted into the page with just a little light
# formatting by hand afterwards.

from common import *
import numpy as np
import stefpack as sp

iform = '{p}/{d}/{d}_2d.fits'

# Number of guard bits.

guard_bits = [2, 1, 0]

# Table header.

table = list()

table.append('|| Name || Guard bits' + ' ||' * 2 * len(guard_bits))
row = '|| ||'
for ng in guard_bits:
    row += ' {} || ||'.format(ng)
table.append(row)
table.append('|| ||' + ' Size || RMS ||' * len(guard_bits))

for d in datasets:

    ifile = iform.format(p=dat_dir, d=d)

    # Read original image.

    size_orig, image_orig = read_image(ifile)

    row = '| {} |'.format(d)

    for ng in guard_bits:

        print('Compressing {} with {} guard bits'.format(d, ng))

        # Quantise image.
        nb, imin, image_quant = sp.quantise(image_orig, ng=ng)

        # Get size of image if it were compressed. 
        size_comp = sp.size_compressed(image_quant)

        # Dequantise image.
        image_comp = sp.dequantise(nb, imin, image_quant)

        # Compute RMS of the difference between compressed image and
        # original.
        rms = np.sqrt(np.mean((image_comp - image_orig)**2))

        print('-> compression factor', size_comp/size_orig, 'rms', rms)

        row += ' {:.3f} | {} |'.format(size_comp/size_orig, pp(rms))

    table.append(row)

# Write table of results.

rfile = '{p}/table_stefpack.txt'.format(p=res_dir)

print('Writing results to', rfile)

with open(rfile, 'w') as f:
    for row in table:
        f.write(row + '\n')
