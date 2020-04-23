# Dan White March 2019-2020
# simpleFlowDecTest.py 
# because the example python script isnt working on my setup
# try this as a simpler more direct test - which seems to work.

# flowdec pip package install/update requirements for anaconda on win10 64 bit:

# install the pip package for flowdec with GPU support as per the flowdec install instructions:
# github.com/hammerlab/flowdec/blob/master/README.md   but......


# 22 april 2020 - what works today :
# flowdec uses tensorflow which on nvidda GPU uses CUDA so need to install the stuff here
# https://www.tensorflow.org/install/gpu   but.....those instructionsd seem to install incompatible stuff... so try
# things were installed in this order and the script works and used the GPU
#cuda toolkit 10.0 
#cudnn-10.0 7.6.34.38 installed into C:/tools/
#pip install flowdec
#     not pip install flowdec[tf_gpu  
# ommitting the tf_gpu option, so it leaves tensorflow-gpu uninstalled, becasue by default
# by now it installs v2.1 of tensorflow which doesnt seem to work for flowdec? 
# pip install tensorflow-gpu==1.14.0 (2.0 might work...? maybe needs higher cuda version)
# Need windows env variables pointing to cuda stuff:  CUDA and CUPTI and another related library cuDNN
# SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin;%PATH%
# SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\extras\CUPTI\libx64;%PATH%
# SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\include;%PATH%
# SET PATH=C:\tools\cuda\bin;%PATH%
# some of these don't seem to be sticky???

from skimage.external.tifffile import imsave, imread
from flowdec import data as fd_data
from flowdec import restoration as fd_restoration

# Load test image from same dir as we execute in
inputImg = 'C1-YeastTNA1_1516_conv_RG_26oC_003sub100.tif'
raw = imread(inputImg)

# Load psf kernel image from same dir
# A cropped 64x64 PSF to reduce memory use, 21 z slices, 0.125 nm spacing in z
PSFsmall = 'gpsf_3D_1514_a3_001_WF-sub105crop64.tif'
# The same PSF but not cropped so much, 128x128, probably uses much more memory.  
PSFbigger = 'gpsf_3D_1514_a3_001_WF-sub105crop128.tif'
# choose the psf to use from the options above. 
PSF = PSFbigger
print (PSF)
kernel = imread(PSF)

# Run the deconvolution process and note that deconvolution initialization is best kept separate from 
# execution since the "initialize" operation corresponds to creating a TensorFlow graph, which is a 
# relatively expensive operation and should not be repeated across multiple executions
n_iter = 250
algo = fd_restoration.RichardsonLucyDeconvolver(raw.ndim).initialize()
res = algo.run(fd_data.Acquisition(data=raw, kernel=kernel), niter=n_iter).data

# save the result,
print('Saving result image TIFF file')
# using skimage.external.tifffile.imsave
imsave(('result' + inputImg + PSF + str(n_iter) + 'iterations.tif'), res)
