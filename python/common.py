import os
import subprocess
import astropy.io.fits as fits

# Data and results directories.

dat_dir = '../data'
res_dir = '../results'

# Datasets.

datasets = [
    '1600+650',
    '3C10-P',
    'Cyg_A-P.model_centre',
    'GLEAM',
    'SKAMid_B1_8h_v3',
    'SKAMid_B2_8h_v3',
    'SKAMid_B5_8h_v3'
]


def read_image(ifile, hdu=0, squeeze=True):
    """Read FITS image and get its size."""

    size = os.path.getsize(ifile)
    with fits.open(ifile) as f:
        image = f[hdu].data
    if squeeze:
        image = image.squeeze()
    return size, image


def pp(x, sigfig=3):
    """Pretty-print a number in scientific notation using wiki markup."""

    s = '{0:.{1:d}e}'.format(x, sigfig)
    m, e = s.split('e')
    e = str(int(e))  # this is to remove leading zeros in the exponent
    s = '{0} × 10 ^{1}^'.format(m, e)
    return s


def run_fpack(ifile, ofile, options='', delete=True):
    """Run fpack on a file and read the image from the compressed file."""

    cform = 'fpack {opt} -O {out} {inp}'
    command = cform.format(opt=options, inp=ifile, out=ofile)
    cout = subprocess.run(command.split(), capture_output=True)
    if cout.returncode == 0:
        size, image = read_image(ofile, hdu=1)
    else:
        size, image = None, None
    if delete and os.path.exists(ofile):
        os.remove(ofile)
    return size, image
