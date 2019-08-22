"""
Dan White 18 March 2019

python script to test pycudadecon from Talley L,
https://github.com/tlambert03/pycudadecon
This script builds on the examples to write the 
result image and OTF as TIFF files. 

pyCUDAdecon python wraps CUDAdecon from Lin Shao / Dan Milkie
HHMI Janelia. 
https://github.com/dmilkie/cudaDecon
which implements an acellerated RL deconvolution algorithm:
D.S.C. Biggs and M. Andrews, 
Acceleration of iterative image restoration algorithms,
Applied Optics, Vol. 36, No. 8, 1997.
https://doi.org/10.1364/AO.36.001766
and implementation on the GPU using CUDA for further speed up.

Requirements to run on windows 10:
requires nvidia GPU with enough ram to hold the images
requires nvidia cuda driver
requires installation of python and other python packlages, 
which are included in the anaconda python release.
pyCUDAdecon and instructions to install and use are at  
https://github.com/tlambert03/pycudadecon
"""

#import required packages
from pycudadecon import decon, make_otf
from skimage.external.tifffile import imsave

# set input a and output file paths
image_path = 'C1-YeastTNA1_1516_conv_RG_26oC_003.tif'
psf_path = 'gpsf_3D_1514_a3_001_WF-sub105.tif'
otfOutPath = 'otf.tif'

# do the deconvolution on GPU
numIters = 15
result = decon(image_path, psf_path, n_iters=numIters)
print("result data type is " + str(result.dtype))
print('results numpy array shape is ')
print(result.shape)

# save the result,
print('Saving result image TIFF file')
# using skimage.external.tifffile.imsave
imsave(('result' + str(numIters) + 'iterations.tif'), result) #, imagej)

# save otf tiff file from PSF image tiff.
print('making otf')
make_otf(psf_path, otfOutPath, dzpsf=0.15, dxpsf=0.05, wavelength=510, na=1.3, nimm=1.333, otf_bgrd=None, krmax=0, fixorigin=10, cleanup_otf=True, max_otf_size=60000)
