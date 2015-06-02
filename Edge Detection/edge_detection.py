# File: edge_detection.py
# Author: Thomas Lesniak
# Date created: 5/20/2015
# Date last modified: 5/20/2015
# Python Version: 2.7 

# References used:
# http://juanreyero.com/article/python/python-convolution.html#sec-1-5
# http://www.catenary.com/howto/diagedge.html 
# http://www.catenary.com/docs/viclibref-l-o.html#matrixconvex
# http://www.catenary.com/docs/viclibref-l-o.html#matrixconv
# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.filters.convolve.html

import numpy as np
from scipy import ndimage
from PIL import Image # used Pillows fork of PIL

"""
	Uses scipys's nd-convolution implementation
	with a given kernel to output an edge-highlighted
	output of the original image. kernel is an 
	NxN square matrix, srcImage and destImg the input
	and output image file names, and grayscale specifies
	whether or not the srcImage is in grayscale (True) or
	RGB (False). 
"""
def edge_detect(kernel, srcImg, destImg, grayscale=True):
	srcArray = array_from_img(srcImg, grayscale)
		
	#convolution with values beyond borders set to 0
	dstArray = ndimage.convolve(srcArray, kernel, mode='constant', cval=0.0)
	img_from_array(norm(dstArray), destImg)
	
	
"""
	Ensure that the image we read is stored 
	as a grayscale array of floats.
"""
def array_from_img(fname, grayscale):
	if not grayscale:
		return np.asarray(Image.open(fname).convert(mode="L"), dtype=np.float32)
	
	return np.asarray(Image.open(fname), dtype=np.float32)

"""
	Save an array as an image, rounding the values 
	back to 8-bit integers.
"""
def img_from_array(array, fname):
	Image.fromarray(array.round().astype(np.uint8)).save(fname)
	
	
"""
	Normalizes the array to help define edge features.
"""
def norm(array):
    return 255. * np.absolute(array) / float(np.max(array))


if __name__ == '__main__':

	# diagonal edge detection
	kernel = np.array(
	[[-5, 0, 0],
	 [ 0, 0, 0],
	 [ 0, 0, 5]])
	 
	edge_detect(kernel, 'tree.jpg', 'tree_diag.jpg')
	edge_detect(kernel, 'lenna.png', 'lenna_diag.png', grayscale=False)
	edge_detect(kernel, 'skyline.jpg', 'skyline_diag.png', grayscale=False)
	
	# horizontal edge detection
	kernel = np.array(
	[[-1, -1, -1],
	 [ 0,  0,  0],
	 [ 1,  1,  1]])
	 
	edge_detect(kernel, 'tree.jpg', 'tree_hor.jpg')
	edge_detect(kernel, 'lenna.png', 'lenna_hor.png', grayscale=False)
	edge_detect(kernel, 'skyline.jpg', 'skyline_hor.png', grayscale=False)
	
	# vertical edge detection
	kernel = np.array(
	[[-1, 0, 1],
	 [-1, 0, 1],
	 [-1, 0, 1]])
	 
	edge_detect(kernel, 'tree.jpg', 'tree_ver.jpg')
	edge_detect(kernel, 'lenna.png', 'lenna_ver.png', grayscale=False)
	edge_detect(kernel, 'skyline.jpg', 'skyline_ver.png', grayscale=False)