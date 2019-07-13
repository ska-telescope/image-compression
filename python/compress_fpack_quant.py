#!/usr/bin/env python3
#
# This script runs fpack on the images to test the effect of the
# quantisation level.  fpack is run on the files using subprocess, and
# the compressed files are read in to compute the RMS errors.
#
# The results are written as a table in Confluence wiki markup, so it
# can be cut and pasted into the page with just a little light
# formatting by hand afterwards.

from common import *
import numpy as np

iform = '{p}/{d}/{d}_2d.fits'
oform = '{p}/{d}/{d}_2d.fits.fz'

# Quantisation levels.

qvalue = [4, 2, 1]
tilesize = 1024

# Table header

table = []

table.append('|| Name || Quantisation Level' + ' ||' * 2 * len(qvalue))
row = '|| ||'
for q in qvalue:
    row += ' {} || ||'.format(q)
table.append(row)
table.append('|| ||' + ' Size || RMS ||' * len(qvalue))

# Loop over datasets.

for d in datasets:

    ifile = iform.format(p=dat_dir, d=d)
    ofile = oform.format(p=dat_dir, d=d)

    # Read original file.

    size_orig, image_orig = read_image(ifile)
    row = '| {} |'.format(d)

    # Loop over q values.

    for q in qvalue:

        print('Compressing {} with quantisation value {}'.format(d, q))

        options = '-t {t},{t} -q {q}'.format(t=tilesize, q=q)
        size_comp, image_comp = run_fpack(ifile, ofile, options=options)
        rms = np.sqrt(np.mean((image_comp - image_orig)**2))

        print('-> compression factor', size_comp/size_orig, 'rms', rms)
        row += ' {:.3f} | {} |'.format(size_comp/size_orig, pp(rms))

    table.append(row)

# Write table of results.

rfile = '{p}/table_fpack_quant.txt'.format(p=res_dir)

print('Writing results to', rfile)

with open(rfile, 'w') as f:
    for row in table:
        f.write(row + '\n')
