"""
Dan White March 2019
simpleFlowDecTest.py 
because the example python script isnt working on my setup
try this as a simpler more direct test - which seems to work.

flowdec anaconda package install/update requirements for anaconda on win10 64 bit:

install the pip package for flowdec with GPU support as per the flowdec install instructions

as of march 2019 numpy and scikit-image need updating to newer versions using conda
	conda install -c anaconda numpy=1.16.0
	conda install -c anaconda scikit-image=0.14.2
as does tensor flow gpu  - the version installed by flowdec have a dll load error. 
watch out for cuda / tensorflow versions compatabiliries. 
	conda install -c anaconda tensorflow-gpu    
I got a load dll error before this install, but tensor flow updated to v1.13 tested ok
"""

from skimage.external.tifffile import imsave, imread
from flowdec import data as fd_data
from flowdec import restoration as fd_restoration

# Load test image from same dir as we execute in
raw = imread('redcell400x400x25.tif')

# Load psf kernel image from same dir
kernel = imread('psfbig.tif')

# Run the deconvolution process and note that deconvolution initialization is best kept separate from 
# execution since the "initialize" operation corresponds to creating a TensorFlow graph, which is a 
# relatively expensive operation and should not be repeated across multiple executions
algo = fd_restoration.RichardsonLucyDeconvolver(raw.ndim).initialize()
res = algo.run(fd_data.Acquisition(data=raw, kernel=kernel), niter=100).data

# save the result,
print('Saving result image TIFF file')
# using skimage.external.tifffile.imsave
imsave('result.tif', res)
