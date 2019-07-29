# Image compression comparison

This repository contains code to compare the performance of
compression algorithms on radio astronomical images.  The algorithms
tested are:

* [Algorithm proposed by Stef Salvini][1]
* FITS image compression, see
  - [FITS tiled image compression convention][2]
  - [fpack and funpack][3]
* [HDF5 compression][4]

The results are in the [SKA Confluence][5].

The directories contain:

* matlab: Stef's original Matlab image compression code
* python: Python implementation of Stef's algorithm and scripts for
  running the tests
* data: FITS images for testing compression algorithms
* results: images and tables for the Confluence page

To run the comparison scripts you need:

* Python with packages
  - numpy
  - matplotlib
  - astropy
  - h5py
* fpack binary from cfitsio (note this is not compiled by default, you
  need to do `make fpack`)

[1]: https://drive.google.com/drive/folders/1JcTRUYsU7px1KMBUgq0H3z9H9Uza9Fro
[2]: https://fits.gsfc.nasa.gov/registry/tilecompression.html
[3]: https://heasarc.gsfc.nasa.gov/fitsio/fpack/
[4]: https://portal.hdfgroup.org/display/HDF5/HDF5
[5]: https://confluence.skatelescope.org/display/SE/Comparison+of+image+compression+methods
