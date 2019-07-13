# Test images

These four images are stored in the repository (using git lfs):

* 1600+650: 4079 x 4079 pixels, 63 MB
* 3C10-P: 1024 x 1024 pixels, 4 MB
* Cyg_A-P.model_centre: 512 x 512 pixels, 1 MB
* GLEAM: 6000 x 6000 pixels, 137 MB (simulated SKA1-Low dirty image,
  from Fred Dulwich)

Each one has a corresponding compressed image data file written by the
Matlab implementation of Stef's algorithm (filename: *_comp.dat).

The other three images are too large for git lfs, so they can be
downloaded with the script `download_images.sh`:

* SKAMid_B1_8h_v3: 32768 x 32768 pixels, 4096 MB (simulated SKA1-Mid
  band 1 image, from SKA Data Challenge)
* SKAMid_B2_8h_v3: 32768 x 32768 pixels, 4096 MB (simulated SKA1-Mid
  band 2 image, from SKA Data Challenge)
* SKAMid_B5_8h_v3: 32768 x 32768 pixels, 4096 MB (simulated SKA1-Mid
  band 5 image, from SKA Data Challenge)
