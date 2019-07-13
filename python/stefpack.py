"""Python implementation of Stef Salvini's image compression algorithm
based on his original Matlab code.

CAVEATS:

- The quantisation of the values sometimes disagrees with the Matlab
  version. This is because the numpy `rint` function behaves
  differently from the Matlab `round` function for values with
  fractional part exactly 0.5 (`round` rounds away from zero, whereas
  `rint` rounds to the nearest even value following the IEEE 754
  floating point standard).

- if you read a file compressed with the Matlab code, you need to
  transpose the image afterwards (the ordering of the pixels is
  different).

"""

import numpy as np


def quantise(image, ng=2, blocksize=32):
    """Quantise image."""

    # Get minimum RMS of image.

    irms = minrms(image, blocksize=blocksize)

    # Compute number of bits and scale factor.

    nb = int(np.floor(1 - np.log2(irms))) + ng
    f1 = 2**nb

    # Scale image and remove offset.

    image_quant = np.rint(f1 * image)
    imin = -np.min(image_quant)
    image_quant += imin
    
    # Convert to integer data types.

    imin = int(imin)
    image_quant = image_quant.astype(np.uint32)
    
    return nb, imin, image_quant


def dequantise(nb, imin, image_quant):
    """Dequantise image."""

    # Convert to float, subtract offset and divide by scale factor.

    image = (image_quant.astype(np.float32) - imin) / (2**nb)

    return image


def size_compressed(image_quant):
    """Calculate size of image in bytes when compressed."""

    # Number of bytes in header (3 x int32, 3 x int64).

    nbytes_head = 36

    # Calculate length of each value in bits, the maximum length, and
    # the number of bits needed to represent the maximum length.

    length = np.ceil(np.log2(image_quant+1)).astype(int)
    maxlen = np.max(length)
    lenbit = int(np.ceil(np.log2(maxlen+1)))

    # Calculate total number of bits in the compressed image.  The
    # bits are stored in a uint32 array, so get its length and its
    # size in bytes.

    nbits_image = lenbit * image_quant.size + np.sum(length)
    lenarr = (nbits_image - 1) // 32 + 1
    nbytes_image = 4 * lenarr

    # Total size.

    nbytes = nbytes_head + nbytes_image

    return nbytes


def write_compressed(filename, nb, imin, image_quant):
    """Compress image and write to file."""

    # Get dimensions of the image array.

    nx, ny = image_quant.shape

    # Get maximum value in array, calculate its length in bits, then
    # calculate the maximum number of bits needed to represent the
    # length.

    maxval = np.max(image_quant)
    maxlen = int(np.ceil(np.log2(maxval+1)))
    lenbit = int(np.ceil(np.log2(maxlen+1)))

    # Set format string for encoding length of values.  This has the same
    # number of bits for all of the pixels.  Its meaning is: padded with
    # zeros, aligned right, width lenbit, binary.

    fmt = '0>{w}b'.format(w=lenbit)

    # Values themselves are variable width, so their format string is
    # simply 'b' below.

    # Loop over image pixels.  The binary data is stored in the string
    # z during the conversion process.  This is done in a sub-optimal
    # way: the entire string is written before converting it into a
    # uint32 array.

    z = ''

    for i in range(nx):
        for j in range(ny):
            value = image_quant[i, j]
            if value == 0:
                # Value is zero, so encode length zero.
                z += format(0, fmt)
            else:
                # Get length
                length = int(np.ceil(np.log2(value+1)))
                # Encode length and value.
                z += format(length, fmt) + format(value, 'b')

    # Get size of uint32 array to hold compressed image.

    lenarr = (len(z) - 1) // 32 + 1

    # Pad string so its length is a multiple of 32.

    npad = 32 * lenarr - len(z)
    z += '0' * npad

    # Convert the string to a uint32 array.

    image_comp = np.zeros(lenarr, dtype=np.uint32)
    for i in range(lenarr):
        image_comp[i] = int(z[32*i:32*(i+1)], base=2)

    # Write data to file.

    with open(filename, 'w') as f:
        np.int64(nx).tofile(f)
        np.int64(nx).tofile(f)
        np.int32(nb).tofile(f)
        np.int32(imin).tofile(f)
        np.int32(lenbit).tofile(f)
        np.int64(lenarr).tofile(f)
        image_comp.tofile(f)


def read_compressed(filename):
    """Read compressed image from file."""

    with open(filename, 'r') as f:
        nx, ny = np.fromfile(f, dtype=np.int64, count=2)
        nb, imin, lenbit = np.fromfile(f, dtype=np.int32, count=3)
        lenarr, = np.fromfile(f, dtype=np.int64, count=1)
        image_comp = np.fromfile(f, dtype=np.uint32, count=lenarr)

    # Array for decompressed image.

    image_quant = np.zeros((nx, ny), dtype=np.uint32)

    # Convert compressed data array to string.

    z = ''
    for i in range(lenarr):
        z += format(image_comp[i], '0>32b')

    # Loop through pixels.

    kmax = 0
    for i in range(nx):
        for j in range(ny):
            # Read length (if it is 0, then the value is 0).
            kmin = kmax
            kmax = kmin + lenbit
            length = int(z[kmin:kmax], base=2)
            if length > 0:
                # Read value.
                kmin = kmax
                kmax = kmin + length
                image_quant[i, j] = int(z[kmin:kmax], base=2)

    return nb, imin, image_quant


def minrms(image, blocksize=32):
    """Find minimum rms of image, calculated block-wise."""

    nx, ny = image.shape
    rmsmin = np.inf

    for imin in range(0, nx, blocksize):
        imax = min(imin + blocksize, nx)
        for jmin in range(0, ny, blocksize):
            jmax = min(jmin + blocksize, ny)
            rms = np.sqrt(np.mean(image[imin:imax, jmin:jmax]**2))
            rmsmin = min(rms, rmsmin)

    return rmsmin
