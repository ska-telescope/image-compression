# Python image compression comparison scripts

Modules:

* `stefpack.py`: Python implementation of Stef's algorithm.

* `common.py`: Common definitions and functions used by all of the
  scripts.

Scripts:

* `rewrite_images.py`: This script must be run before the others. It
  rewrites the test images as 2-dimensional FITS images.

  The need for this comes from an annoying limitation of astropy. Most
  of the images are 4-dimensional, with frequency and polarisation
  axes too, even if the size along these axes is 1. fpack will happily
  compress 4-dimensional images, but the scripts use astropy to read
  them afterwards, and it will only handle compressed images with up
  to 3 dimensions.

* `plot_images.py`: Plots the test images.

* `compress_stefpack.py`: Runs stefpack compression to test the effect
  of varying the number of guard bits.

* `compress_fpack_quant.py`: Runs fpack compression to test the effect
  of varying the quantisation value.

* `compress_fpack_tiles.py`: Runs fpack compression to test the effect
  of varying the tile shape.

* `test_stefpack.py`: Tests stefpack against a compressed file written
  by the Matlab code.

  The quantised values sometimes disagree because the rounding of
  values with fractional part 0.5 is implemented differently in Matlab
  and numpy. Matlab rounds away from zero, whereas numpy rounds to the
  nearest even value following the IEEE 754 floating point standard.
