#NASA Plant Code

import numpy as np
from numpy import matrix
import cv2
import matplotlib.pyplot as plt

####
####
#1 - HSV and K means
####
####

#Import image from specific location in computer files
im = cv2.imread('i7.png')

#Put gaussian blur on image
im1 = cv2.GaussianBlur(im,(9,9),2)

#Change color space from bgr to hsv
im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2HSV)

#Make image with 3 kmeans
im1_1 = np.float32(im1.reshape((-1,3)))
criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,10,1.0)
K = 3
ret,label,center=cv2.kmeans(im1_1,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
im1_2 = center[label.flatten()]
im1 = im1_2.reshape((im1.shape))

#Put back into bgr from hsv
im1 = cv2.cvtColor(im1,cv2.COLOR_HSV2BGR)

#Count plant pixels - looks for colors in the dark purple region
plant_pixel_1 = cv2.inRange(im1,np.array([40,30,40]),np.array([120,90,120]))
plant_pixel_no_1 = cv2.countNonZero(plant_pixel_1)

#Count reference pixels - looks in the orange region
ref_pixel_1 = cv2.inRange(im1,np.array([220,110,30]),np.array([260,180,80]))
ref_pixel_no_1 = cv2.countNonZero(ref_pixel_1)

#Calculate area per pixel, then find canopy area
pixel_area_1 = 1/ref_pixel_no_1 #inches in^2
area1 = pixel_area_1*plant_pixel_no_1 #inches in^2

#Make original image only within kmean for leaf area, background pixels
#are made to be blue
im12 = im
ind1 = list(range(im12.shape[0]))
ind2 = list(range(im12.shape[1]))
for i in ind1:
    for k in ind2:
        if (plant_pixel_1[i,k] == 0 and ref_pixel_1[i,k] == 0):
            im12[i,k,:] = [255,255,255]
        else:
            im12[i,k,:] = im12[i,k,:]

####
####
#2 - LAB Coloration
####
####

#Put image into LAB colorspace
im2 = cv2.cvtColor(im12,cv2.COLOR_BGR2LAB)

#Get 8 Kmeans
im2_1 = np.float32(im2.reshape((-1,3)))
criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,10,1.0)
K = 8
ret,label,center=cv2.kmeans(im2_1,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
im2_2 = center[label.flatten()]
im2 = im2_2.reshape((im.shape))

#Filter out grey pixels using range in LAB
im21=im2
grey_pixel = cv2.inRange(im21,np.array([100,0,115]),np.array([195,255,255]))
for i in ind1:
    for k in ind2:
        if grey_pixel[i,k] == 255:
            im21[i,k,:] = [136,208,193]
        elif plant_pixel_1[i,k] == 0:
            im21[i,k,:] = im21[i,k,:]

#Put image back into BGR
im24 = cv2.cvtColor(im21,cv2.COLOR_LAB2BGR)

#2 Kmeans, one will be the background blue
im25_1 = np.float32(im24.reshape((-1,3)))
criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,10,1.0)
K = 2
ret,label,center=cv2.kmeans(im25_1,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
im25_2 = center[label.flatten()]
im25 = im25_2.reshape((im.shape))

#Calculate new area
plant_pixel_2 = cv2.inRange(im24,np.array([0,0,0]),np.array([254,254,254]))
plant_pixel_no_2 = cv2.countNonZero(plant_pixel_2)
area2 = pixel_area_1*plant_pixel_no_2

#Compare before and after additional analysis
for i in ind1:
    for k in ind2:
        if plant_pixel_2[i,k] == 0:
            im25[i,k,:] = [255,255,255]
        elif plant_pixel_2[i,k] == 255:
            im25[i,k,:] = im[i,k,:]

####
####
#3 - Canny Edge Detection
####
####

im = cv2.imread('i7.png')

#Put original image into grayscale, apply filter
#im31 = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(im,11,17,17)

#Apply canny edge detection, dilate and erode in order to fill gaps
edged = cv2.Canny(gray,40,55)
edged = cv2.dilate(edged,None,iterations=1)
edged = cv2.erode(edged,None,iterations=1)

#Find countour edges from canny edge detection
im32,contours,hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(im,contours,-1,(255,255,255),0)

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

#Find area of plant (largest) and square (second largest)
#Calculate canopy area
reference_area_3 = nonzero_areas[0]
plant_pixel_3 = np.sum(nonzero_areas[1:len(nonzero_areas)])
area3 = plant_pixel_3/reference_area_3

plant_pixel_3 = np.where(cim==[255,255,255],1,0)
im41 = im
im42 = cv2.imread('i7.png')
ind1 = list(range(im41.shape[0]))
ind2 = list(range(im41.shape[1]))
for i in ind1:
    for k in ind2:
        if plant_pixel_3[i,k,0] == 0:
            im41[i,k,:] = [255,255,255]
        elif plant_pixel_3[i,k,0] == 1:
            im41[i,k,:] = im41[i,k,:]

####
####
#4 - BGR Coloration
####
####

ref_pixel_4 = cv2.inRange(im41,np.array([220,110,30]),np.array([260,180,80]))
im_sub = np.empty([len(ind1),len(ind2)])
for i in ind1:
    for k in ind2:
        im_sub[i,k] = int(im41[i,k,1])/(int(im41[i,k,0])+int(im41[i,k,1])+int(im41[i,k,2])+1)
        if ((im_sub[i,k]>0.31 and im41[i,k,0]>90) or (int(im41[i,k,0])-int(im41[i,k,2]))>85): #or im2[i,k,1]>im2[i,k,2] or int(im2[i,k,1])-int(im2[i,k,0]))>10:
            im42[i,k,:] = [255,255,255]
for i in ind1:
    for k in ind2:
        if ref_pixel_4[i,k] == 255:
            im42[i,k,:] = im41[i,k,:]
        
plant_pixel_4 = cv2.inRange(im42,np.array([0,0,0]),np.array([254,254,254]))
plant_pixel_no_4 = cv2.countNonZero(plant_pixel_4)
area4 = plant_pixel_no_4/reference_area_3

im = cv2.imread('i7.png')
im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
im12 = cv2.cvtColor(im12,cv2.COLOR_BGR2RGB)
im25 = cv2.cvtColor(im25,cv2.COLOR_BGR2RGB)
im41 = cv2.cvtColor(im41,cv2.COLOR_BGR2RGB)
im42 = cv2.cvtColor(im42,cv2.COLOR_BGR2RGB)

plt.subplot(2,5,1)
plt.imshow(im,'gray')
plt.title('Original Image',fontsize=9)
plt.xticks([])
plt.yticks([])
plt.subplot(2,5,2)
plt.imshow(im12,'gray')
plt.title('K Means and HSV Analysis',fontsize=9)
plt.xticks([])
plt.yticks([])
plt.xlabel('Canopy area = %0.02f in^2' %area1,fontsize=7)
plt.subplot(2,5,3)
plt.imshow(im25,'gray')
plt.title('LAB Coloration Analysis + K Mean,HSV',fontsize=9)
plt.xticks([])
plt.yticks([])
plt.xlabel('Canopy area = %0.02f in^2' %area2,fontsize=7)
plt.subplot(2,5,4)
plt.imshow(im41,'gray')
plt.title('Canny Edge Detection',fontsize=9)
plt.xticks([])
plt.yticks([])
plt.xlabel('Canopy area = %0.02f in^2' %area3,fontsize=7)
plt.subplot(2,5,5)
plt.imshow(im42,'gray')
plt.title('RGB Coloration Analysis + Canny Edge',fontsize=9)
plt.xticks([])
plt.yticks([])
plt.xlabel('Canopy area = %0.02f in^2' %area4,fontsize=7)
plt.show()









