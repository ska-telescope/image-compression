#!/bin/bash

# Make directories.

mkdir SKAMid_B1_8h_v3 SKAMid_B2_8h_v3 SKAMid_B5_8h_v3

# Download files.

curl -o SKAMid_B1_8h_v3/SKAMid_B1_8h_v3.fits https://owncloud.ia2.inaf.it/index.php/s/H1rAR0A9qmXBbB5/download
curl -o SKAMid_B2_8h_v3/SKAMid_B2_8h_v3.fits https://owncloud.ia2.inaf.it/index.php/s/FS2pmOFQCn2yL06/download
curl -o SKAMid_B5_8h_v3/SKAMid_B5_8h_v3.fits https://owncloud.ia2.inaf.it/index.php/s/EghzfsEf1CGXVsH/download
