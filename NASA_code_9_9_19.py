#NASA Plant Code
#Noah Weyrick.6

import numpy as np
from numpy import matrix
import cv2
import matplotlib.pyplot as plt

####
####
#Contour and canny edge detection
####
####

#Import image from specific location in computer files, make figure and print image
im = cv2.imread('i7.png')
fig1 = plt.figure(1)
fig1.suptitle('Contouring and Canny Edge Detection',
             fontsize = 14,fontweight = 'bold')
plt.subplot(221)
plt.title('Original Image')
plt.imshow(im,'gray')
plt.xticks([])
plt.yticks([])

#Put original image into grayscale, apply filter
im_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(im_gray,11,17,17)

#Apply canny edge detection, dilate and erode in order to fill gaps
edged = cv2.Canny(gray,40,55)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
plt.subplot(222)
plt.title('Canny Edge Detection')
plt.imshow(edged,'gray')
plt.xticks([])
plt.yticks([])

#Find countour edges from canny edge detection
im2,contours,hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(im,contours,-1,(255,255,255),0)
plt.subplot(223)
plt.title('Contours')
plt.imshow(im)
plt.xticks([])
plt.yticks([])

#Find areas of all contours, concatenate into a list
#Find values above range, sort based on size
areas = []
nonzero_areas = []
cim = np.zeros_like(im)
for i in range(len(contours)):
    areas.append(cv2.contourArea(contours[i]))
    if areas[i] > 1000:
        nonzero_areas.append(areas[i])
        cv2.drawContours(cim,contours,i,(255,255,255),-1)
nonzero_areas.sort()

#Find area of plant (largest) and square (second largest), sum smaller areas
#Calculate canopy area
reference_area = nonzero_areas[0]
pre_largest_area = nonzero_areas[-1]
largest_area = pre_largest_area/reference_area
ax1 = fig1.add_subplot(224)
ax1.text(0.5,0.5,"The largest canopy area is %0.02f in^2" %largest_area,verticalalignment='center',
        horizontalalignment='center',fontsize=10)
plt.xticks([])
plt.yticks([])
plt.box(on=None)
plt.show()

####
####
#LAB coloration analysis
####
####

fig2 = plt.figure(2)

plant_pixel = np.where(cim==[255,255,255],1,0)
im2 = im
ind1 = list(range(im2.shape[0]))
ind2 = list(range(im2.shape[1]))
for i in ind1:
    for k in ind2:
        if plant_pixel[i,k,0] == 0:
            im2[i,k,:] = [255,255,255]
        elif plant_pixel[i,k,0] == 1:
            im2[i,k,:] = im2[i,k,:]

im3 = cv2.cvtColor(im2,cv2.COLOR_RGB2LAB)
im4=im3

grey_pixel = cv2.inRange(im4,np.array([130,0,115]),np.array([200,150,255]))
for i in ind1:
    for k in ind2:
        if grey_pixel[i,k] == 255:
            im4[i,k,:] = [255,128,128]
        elif grey_pixel[i,k] == 0:
            im4[i,k,:] = im4[i,k,:]

im5 = cv2.cvtColor(im4,cv2.COLOR_LAB2BGR)
plt.title('Output Image')
plt.imshow(im5,'gray')
plt.xticks([])
plt.yticks([])
plt.show()

