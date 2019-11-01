#NASA Plant Code
#Noah Weyrick.6

import numpy as np
from numpy import matrix
import cv2
import matplotlib.pyplot as plt

####
####
#Canopy Area
####
####

#Import image from specific location in computer files
im = cv2.imread('C:/Users/no_we/Downloads/i6.jpg')

#Create figure with 3x2 subplot
#Print image 1 (original)
fig = plt.figure(1)
fig.suptitle('Image Processing - Leaf Canopy Area',
             fontsize = 14,fontweight = 'bold')
plt.subplot(321)
plt.title('Original',fontsize=10)
plt.imshow(im,'gray')
plt.xticks([]) #removes ticks from figure plots
plt.yticks([])

#Put gaussian blur on image
im2 = cv2.GaussianBlur(im,(9,9),2)

#Print image 2 (gauss)
plt.subplot(322)
plt.title('Gaussian Blur',fontsize=10)
plt.imshow(im2,'gray')
plt.xticks([])
plt.yticks([])

#Change color space from bgr to hsv
im3 = cv2.cvtColor(im2,cv2.COLOR_BGR2HSV)

#Print image 3 (hsv + gauss)
plt.subplot(323)
plt.title('BGR to HSV',fontsize=10)
plt.imshow(im3,'gray')
plt.xticks([])
plt.yticks([])

#Make image with 3 kmeans
im4_1 = np.float32(im3.reshape((-1,3)))
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret,label,center=cv2.kmeans(im4_1,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
im4_2 = center[label.flatten()]
im4 = im4_2.reshape((im3.shape))

#Print image 4 (kmeans applied)
plt.subplot(324)
plt.title('3 Kmeans in HSV',fontsize=10)
plt.imshow(im4,'gray')
plt.xticks([])
plt.yticks([])

#Put back into bgr from hsv
im5 = cv2.cvtColor(im4, cv2.COLOR_HSV2BGR)

#Print image 5 (kmeans + gauss + bgr)
plt.subplot(325)
plt.title('HSV to BGR',fontsize=10)
plt.imshow(im5,'gray')
plt.xticks([])
plt.yticks([])

#Count plant pixels - looks for colors in the dark purple region
plant_pixel = cv2.inRange(im5,np.array([40,30,40]),np.array([120,90,120]))
plant_pixel_no = cv2.countNonZero(plant_pixel)

#Count reference pixels - looks in the orange region
ref_pixel = cv2.inRange(im5,np.array([220,110,30]),np.array([260,180,80]))
ref_pixel_no = cv2.countNonZero(ref_pixel)

#Calculate area per pixel, then find canopy area
pixel_area = 1/ref_pixel_no #inches in^2
area = pixel_area*plant_pixel_no #inches in^2

#Print text showing the calculated area
ax = fig.add_subplot(326)
ax.text(0.5,0.5,"The canopy area is %0.02f in^2" %area,verticalalignment='center',
        horizontalalignment='center',fontsize=10)
plt.xticks([])
plt.yticks([])
plt.box(on=None)
plt.show()

####
####
#Color Analysis
####
####

#Make image 6, original image only within kmean for leaf area, background pixels
#are made to be blue
im6 = im
ind1 = list(range(im6.shape[0]))
ind2 = list(range(im6.shape[1]))
for i in ind1:
    for k in ind2:
        if plant_pixel[i,k] == 0:
            im6[i,k,:] = [0,0,255]
        elif plant_pixel[i,k] == 255:
            im6[i,k,:] = im6[i,k,:]

#Put image into LAB colorspace
im7 = cv2.cvtColor(im6,cv2.COLOR_BGR2LAB)

#10 Kmeans
im7_1 = np.float32(im7.reshape((-1,3)))
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 10 #6 or less better for i4, 10 or more better for i2, 8 otherwise
ret,label,center=cv2.kmeans(im7_1,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
im7_2 = center[label.flatten()]
im7 = im7_2.reshape((im.shape))

#Print image 7
fig = plt.figure(2)
fig.suptitle('Additional Analysis',fontsize = 14,fontweight = 'bold')
plt.subplot(221)
plt.title('LAB, 10 Kmeans',fontsize=8)
plt.imshow(im7,'gray')
plt.xticks([])
plt.yticks([])

#Filter out grey pixels using range in LAB
im8=im7
grey_pixel = cv2.inRange(im8,np.array([100,0,115]),np.array([195,255,255]))
for i in ind1:
    for k in ind2:
        if grey_pixel[i,k] == 255:
            im8[i,k,:] = [136,208,193]
        elif plant_pixel[i,k] == 0:
            im8[i,k,:] = im8[i,k,:]

#Put image back into BGR
im9 = cv2.cvtColor(im8,cv2.COLOR_LAB2BGR)

#2 Kmeans, one will be the background blue
im10_1 = np.float32(im9.reshape((-1,3)))
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 2
ret,label,center=cv2.kmeans(im10_1,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
im10_2 = center[label.flatten()]
im10 = im10_2.reshape((im.shape))

#Print image 10
plt.subplot(222)
plt.title('BGR, Removed Grey, 2 Kmeans',fontsize=8)
plt.imshow(im10,'gray')
plt.xticks([])
plt.yticks([])

#Turn the pixel value matrix of the image into a list using concatenation
for i in ind1:
    if i == 0:
        pixel_list = im10[0]
    else:
        pixel_list = np.concatenate((pixel_list,im10[i]),axis=0)
fmax = pixel_list.max(0)
fmin = pixel_list.min(0)

#Print average pixel value for the plant in bgr
plt.subplot(223)
plt.title('The average plant color in BGR is {} {} {}'
           .format(fmax.item(0),fmax.item(1),fmin.item(2)),fontsize=6)
plt.xticks([])
plt.yticks([])
plt.box(on=None)

#Calculate new area
new_plant_pixel = cv2.inRange(im9,np.array([0,0,0]),np.array([254,254,254]))
new_plant_pixel_no = cv2.countNonZero(new_plant_pixel)
new_area = pixel_area*new_plant_pixel_no

#Print new area
plt.subplot(224)
plt.title('The newly calculated canopy area is %0.02f in^2' %new_area,fontsize=6)
plt.xticks([])
plt.yticks([])
plt.box(on=None)
plt.show()

#Compare before and after additional analysis
for i in ind1:
    for k in ind2:
        if new_plant_pixel[i,k] == 0:
            im10[i,k,:] = [0,0,255]
        elif new_plant_pixel[i,k] == 255:
            im10[i,k,:] = im[i,k,:]
im11=im10
im6 = cv2.cvtColor(im6,cv2.COLOR_BGR2RGB)
im11 = cv2.cvtColor(im11,cv2.COLOR_BGR2RGB)
fig = plt.figure(3)
fig.suptitle('Additional Analysis',fontsize = 14,fontweight = 'bold')
plt.subplot(121)
plt.title('Before')
plt.imshow(im6,'gray')
plt.xlabel('The old calculated canopy area is %0.02f in^2' %area,fontsize=6)
plt.xticks([])
plt.yticks([])
plt.subplot(122)
plt.title('After')
plt.imshow(im11,'gray')
plt.xlabel('The newly calculated canopy area is %0.02f in^2' %new_area,fontsize=6)
plt.xticks([])
plt.yticks([])
plt.show()


