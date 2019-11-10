#NASA Plant Code
#Noah Weyrick.6

import numpy as np
from numpy import matrix
import cv2
import matplotlib.pyplot as plt

####
####
#Image Correction
####
####

#https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
#120 angle lens correction
DIM=(3024,4032)
K=np.array([[2414.9662,0.0,1474.9274],[0.0,2422.8611,1983.4191],[0.0,0.0,1.0]])
D=np.array([[0.27388],[-0.570613],[0.602927],[-0.379167]])
balance = 1
im = cv2.imread('i15.jpg')
dim1 = im.shape[:2][::-1]
dim2 = dim1
dim3 = dim1
scaled_K = K*dim1[0]/DIM[0]
scaled_K[2][2] = 1.0  
new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K,D,dim2,np.eye(3),balance=balance)
map1,map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K,D,np.eye(3),new_K,dim3,cv2.CV_16SC2)
im = cv2.remap(im,map1,map2,interpolation=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
im = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
plt.imshow(im,'gray')
plt.show()
