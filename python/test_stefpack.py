#!/usr/bin/env python3
#
# Test stefpack implementation against file written by Matlab code.

from common import *
import os
import stefpack as sp

dataset = 'Cyg_A-P.model_centre'
ng = 0

iform = '{p}/{d}/{d}_2d.fits'
oform = '{p}/{d}/{d}.dat'
mform = '{p}/{d}/{d}_comp.dat'

ifile = iform.format(p=dat_dir, d=dataset)
ofile = oform.format(p=dat_dir, d=dataset)
mfile = mform.format(p=dat_dir, d=dataset)

print('Reading original image from', ifile)

_, image_orig = read_image(ifile)

print('Image shape:', image_orig.shape)

print('Quantising image')

# Use matlab_round=True to exactly mimic Matlab behaviour.

nb, imin, image_quant = sp.quantise(image_orig, ng=ng,
                                    matlab_round=True)

print('nb:', nb)
print('imin:', imin)
print('image:')
print(image_quant)

print('Size when compressed:', sp.size_compressed(image_quant), 'bytes')

print('Writing compressed image to', ofile)

sp.write_compressed(ofile, nb, imin, image_quant)

print('Reading compressed image from', ofile)

nb_read, imin_read, image_quant_read = sp.read_compressed(ofile)

print('nb:', nb_read)
print('imin:', imin_read)
print('image:')
print(image_quant_read)

print('nb good:', nb_read == nb)
print('imin good:', imin_read == imin)
print('image good:', (image_quant_read == image_quant).all())

# Remove test file.

if os.path.exists(ofile):
    os.remove(ofile)

print('Reading image compressed with Matlab from', mfile)

nb_mat, imin_mat, image_quant_mat = sp.read_compressed(mfile)

# NB need to transpose the image read from Matlab file.

print('nb', nb_mat)
print('imin', imin_mat)
print('image')
print(image_quant_mat.T)

print('nb good', nb_mat == nb)
print('imin good:', imin_mat == imin)
i = image_quant_mat.T != image_quant
nbad = i.sum()
if nbad > 0:
    print(nbad, 'pixels disagree')
    print('Original image values:', image_orig[i])
    print('Scaled image values:', (2**nb)*image_orig[i])
    print('Quantised image values (minus offset)', image_quant[i]-imin)
    print('Matlab quantised image values (minus offset)', image_quant_mat.T[i]-imin)
else:
    print('image good:', True)
