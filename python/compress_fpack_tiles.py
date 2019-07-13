#!/usr/bin/env python3
#
# This script runs fpack on the images to test the effect of the tile
# sizes.  fpack is run on the files using subprocess, and the
# resulting compressed files are read in to compute the RMS errors.
#
# The results are written as a table in Confluence wiki markup, so it
# can be cut and pasted into the page with just a little light
# formatting by hand afterwards.

from common import *
import numpy as np

iform = '{p}/{d}/{d}_2d.fits'
oform = '{p}/{d}/{d}_2d.fits.fz'

# Tile sizes.
#
# Two fixed sizes: row-by-row (the default, so no flags), and the
# whole image.

tileopts = [('Row', ''), ('Whole image', '-w')]

# Square tile sizes, which are appended to the tileopts list.

tilesize = [256, 512, 1024]

for t in tilesize:
    tileopts.append(('{t} × {t}'.format(t=t),
                     '-t {t},{t}'.format(t=t)))

# Table header.

table = list()

table.append('|| Name || Tile size' + ' ||' * 2 * len(tileopts))
row = '|| ||'
for name, _ in tileopts:
    row += ' {} || ||'.format(name)
table.append(row)
table.append('|| ||' + ' Size || RMS ||' * len(tileopts))

# Loop over datsets.

for d in datasets:

    ifile = iform.format(p=dat_dir, d=d)
    ofile = oform.format(p=dat_dir, d=d)

    # Read original file.

    size_orig, image_orig = read_image(ifile)

    row = '| {} |'.format(d)

    # Loop over tile sizes.

    for _, opts in tileopts:

        print('Compressing {} with tile options {}'.format(d, opts))
        size_comp, image_comp = run_fpack(ifile, ofile, options=opts)
        if size_comp is None:
            print('-> compression failed')
            row += ' - | - |'
        else:
            rms = np.sqrt(np.mean((image_comp - image_orig)**2))
            print('-> compression factor', size_comp/size_orig, 'rms', rms)
            row += ' {:.3f} | {} |'.format(size_comp/size_orig, pp(rms))
            
    table.append(row)

# Write table of results.

rfile = '{p}/table_fpack_tiles.txt'.format(p=res_dir)

print('Writing results to', rfile)

with open(rfile, 'w') as f:
    for row in table:
        f.write(row + '\n')
