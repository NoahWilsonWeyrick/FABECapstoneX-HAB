import numpy as np
from numpy import matrix
import cv2
import matplotlib.pyplot as plt

#Correction for 140 degree rasp pi lens, one photo at a time

image = r'' #Insert image directory
im = cv2.imread(image)

DIM=(1920, 1080)
K=np.array([[823.5189495942238, 0.0, 885.9562421876449], [0.0, 823.5085569859503, 573.8293949955043], [0.0, 0.0, 1.0]])
D=np.array([[-0.11014552169213372], [0.46737662046831663], [-1.0066309873708785], [0.7545082914715061]])
balance = 1
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
plt.xticks([])
plt.yticks([])
plt.show()
