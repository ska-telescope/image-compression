#!/usr/bin/env python3
#
# This script is a toy example of combining compressed images. The
# test images contain Gaussian noise only, and are combined in three
# different ways:
#
#   1) without quantisation
#   2) with quantisation
#   3) with quantisation and subtractive dithering
#
# In each case it plots histograms of the distribution of pixel values
# for one of the input images and the output image.

from common import res_dir

import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

sigma = 1.0
q = 4.0
nobs = 25
npix = 1_000_000
oform = '{p}/noise_dist_{t}_{c}.png'

# Set quantisation scale.

delta = sigma / q

print('Drawing noise realisations and offsets')

noise1_inp = sigma * np.random.randn(npix, nobs)
off = np.random.rand(npix, nobs) - 0.5

print()
print('Combining images')
print('Case 1: without quantisation')

noise1_out = np.mean(noise1_inp, axis=1)

print('Case 2: with quantisation (q = {})'.format(q))

noise2_inp = np.rint(noise1_inp / delta) * delta
noise2_out = np.mean(noise2_inp, axis=1)

print('Case 3: with quantisation (q = {}) and subtractive dithering'.format(q))

noise3_inp = (np.rint(noise1_inp / delta - off) + off) * delta
noise3_out = np.mean(noise3_inp, axis=1)

print()
print('Input image standard deviation (and ratio to case 1)')

std1_inp = np.std(noise1_inp)
std2_inp = np.std(noise2_inp)
std3_inp = np.std(noise3_inp)

print('Case 1: {}'.format(std1_inp))
print('Case 2: {} {}'.format(std2_inp, std2_inp/std1_inp))
print('Case 3: {} {}'.format(std3_inp, std3_inp/std1_inp))

print()
print('Output image standard deviation (and ratio to case 1)')

std1_out = np.std(noise1_out)
std2_out = np.std(noise2_out)
std3_out = np.std(noise3_out)

print('Case 1: {}'.format(std1_out))
print('Case 2: {} {}'.format(std2_out, std2_out/std1_out))
print('Case 3: {} {}'.format(std3_out, std3_out/std1_out))

print()
print('Making plots')

# Plot noise distribution in first input image.

nbin = 2 * int(nobs/delta) + 1
xmax = 2.5 * (1 + 1.0/nbin)
xmin = -xmax
bins = np.linspace(xmin, xmax, nbin+1)

plt.figure(dpi=250)
plt.title('Input noise distribution without quantisation')
plt.hist(noise1_inp[:, 0], bins=bins)
plt.xlim(xmin, xmax)
ofile = oform.format(p=res_dir, t='inp', c='1')
plt.savefig(ofile)

plt.figure(dpi=250)
plt.title('Input noise distribution with quantisation')
plt.hist(noise2_inp[:, 0], bins=bins)
plt.xlim(xmin, xmax)
ofile = oform.format(p=res_dir, t='inp', c='2')
plt.savefig(ofile)

plt.figure(dpi=250)
plt.title('Input noise distribution with quantisation and subtractive dithering')
plt.hist(noise3_inp[:, 0], bins=bins)
plt.xlim(xmin, xmax)
ofile = oform.format(p=res_dir, t='inp', c='3')
plt.savefig(ofile)

# Plot noise distribution in output image.

nbin = 2 * int(nobs/delta) + 1
xmax = 0.5 * (1 + 1.0/nbin)
xmin = -xmax
bins = np.linspace(xmin, xmax, nbin+1)

plt.figure(dpi=250)
plt.title('Output noise distribution without quantisation')
plt.hist(noise1_out, bins=bins)
plt.xlim(xmin, xmax)
ofile = oform.format(p=res_dir, t='out', c='1')
plt.savefig(ofile)

plt.figure(dpi=250)
plt.title('Output noise distribution with quantisation')
plt.hist(noise2_out, bins=bins)
plt.xlim(xmin, xmax)
ofile = oform.format(p=res_dir, t='out', c='2')
plt.savefig(ofile)

plt.figure(dpi=250)
plt.title('Output noise distribution with quantisation and subtractive dithering')
plt.hist(noise3_out, bins=bins)
plt.xlim(xmin, xmax)
ofile = oform.format(p=res_dir, t='out', c='3')
plt.savefig(ofile)
