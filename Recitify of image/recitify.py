import cv2
import glob
import argparse
import math
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
import os.path
from scipy import ndimage
import os

left = cv2.imread('L.png', cv2.IMREAD_UNCHANGED)
right = cv2.imread('R.png', cv2.IMREAD_UNCHANGED)
# left = (left/256).astype('uint8')
# right = (right/256).astype('uint8')
#left_colour = cv2.cvtColor(left, cv2.COLOR_BayerRG2BGR)
#right_colour = cv2.cvtColor(right, cv2.COLOR_BayerRG2BGR)


cameraMatrix1 = np.array(
    [[1478.4616, 0.0, 940.78233], [0.0, 1474.45028, 679.50984], [0.0,0.0,1.0]])
cameraMatrix2 = np.array(
    [[1478.97446, 0.0, 943.87355], [0.0, 1477.70023, 712.14069], [0.0,0.0,1.0]])
distCoeffs1 = np.array(
    [0.34404, 0.39925000000000005, -0.0024600000000000004, -0.01072, 0.0])
distCoeffs2 = np.array(
    [0.28774000000000005, 0.6423000000000001, 0.00022, -0.0024200000000000003, 0.0])
rotationMatrix = np.array([[0.99973106,   0.01154131,    	0.02018957],
                           [-0.01171467,  0.99989738,    	0.00861916],
                           [-0.02009047,  -0.00885182,    	0.99975736]])

transVector = np.array([29.96389633009774, 0.5883268401189343, -5.0370190999346365])

flags = cv2.CALIB_ZERO_DISPARITY
image_size = left.shape[::-1]

R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, image_size,
                                                  rotationMatrix, transVector, flags=flags)

leftmapX, leftmapY = cv2.initUndistortRectifyMap(cameraMatrix1, distCoeffs1, R1, P1, image_size, cv2.CV_32FC1)
rightmapX, rightmapY = cv2.initUndistortRectifyMap(cameraMatrix2, distCoeffs2, R2, P2, image_size, cv2.CV_32FC1)

left_remap = cv2.remap(left, leftmapX, leftmapY, cv2.INTER_LANCZOS4)
right_remap = cv2.remap(right, leftmapX, rightmapY, cv2.INTER_LANCZOS4)

# For some reason, the images get rotated upside down after remapping, and I have to invert them back
left_remap = ndimage.rotate(left_remap, 180)
right_remap = ndimage.rotate(right_remap, 180)

for line in range(0, int(right_remap.shape[0] / 20)):
    left_remap[line * 20, :] = 0
    right_remap[line * 20, :] = 0

cv2.namedWindow('output images', cv2.WINDOW_NORMAL)
cv2.imshow('output images', np.hstack([left_remap, right_remap]))
cv2.imwrite('recitified_original_color.png',np.hstack([left_remap, right_remap]))
