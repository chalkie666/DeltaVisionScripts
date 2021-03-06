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

import time
import sys

#send output to a log file
sys.stdout = open('FlowDecLog.txt', 'w')

startImports = time.process_time()   
from skimage.external.tifffile import imsave, imread
from flowdec import data as fd_data
from flowdec import restoration as fd_restoration
importsTime = (time.process_time() - startImports)

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

#base number of iterations - RL converges slowly so need tens of iterations or maybe hundreds. 
base_iter = 10

# Run the deconvolution process and note that deconvolution initialization is best kept separate from 
# execution since the "initialize" operation corresponds to creating a TensorFlow graph, which is a 
# relatively expensive operation and should not be repeated across multiple executions

# initialize the TF graph for the deconvolution settings in use for certain sized input and psf images
# works for doing the same input data multiple times with different iteractions
# should work for doing different input data with same sizes of image and psf, 
# eg a time series split into tiff 1 file per time point???? 
startAlgoinit = time.process_time()   
algo = fd_restoration.RichardsonLucyDeconvolver(raw.ndim).initialize()
TFinitTime = (time.process_time() - startAlgoinit)


# run the deconvolution itself
# in a loop making diffrent numbers of iterations, multiples of base value of n_iter
multiRunFactor = 15
timingListIter = []
timingListTime = []
for i in range(1, multiRunFactor+1):
  niter = (base_iter*i)
  # start measuring time
  startDec = time.process_time()
  res = algo.run(fd_data.Acquisition(data=raw, kernel=kernel), niter=(niter)).data
  # measure time here includes only the deconvolution, no file saving
  DecTime = (time.process_time() - startDec)
  # save the result # using skimage.external.tifffile.imsave
  resultFileName = ('result' + inputImg + PSF + str(niter) + 'iterations.tif')
  imsave(resultFileName, res)
  # measure time here includes file saving
  #DecTime = (time.process_time() - startDec)
  print('Saved result image TIFF file' + resultFileName)
  print(str(DecTime) + ' is how many sec ' + str(niter) + ' iterations took.')
  timingListIter.append(niter)
  timingListTime.append(DecTime)

#benchmarking data output
print (str(importsTime) + ' seconds to import flowdec, TF and CUDA libs etc.')
print (str(TFinitTime) + ' sec is the tensorFlow initialisation time')
print ('Pairs of values of iterations done vs time in seconds')
print (timingListIter)
print (timingListTime)
print('Done')