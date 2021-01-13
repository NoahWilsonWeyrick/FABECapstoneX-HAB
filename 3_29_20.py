import numpy as np
from numpy import matrix
import cv2
import matplotlib.pyplot as plt

###This program uses LAB coloration analysis to differentiate between plant canopy and background
###This program will find the percentage of the image taken up by the plant canopy, one image at a time
###This will help to find a correlation between the height of the plants and the percentage of take up
###This process is called stereo vision, which will allow images from two different heights to help estimate plant height

image = r'' #Insert image directory
im = cv2.imread(image)
im_lab = cv2.cvtColor(im,cv2.COLOR_BGR2LAB) #Convert to LAB color space
im_lab = cv2.GaussianBlur(im_lab,(5,5),0)

#Apply LAB coloration analysis
ind1 = list(range(im.shape[0]))
ind2 = list(range(im.shape[1]))
im_l = np.empty([len(ind1),len(ind2)])
im_a = np.empty([len(ind1),len(ind2)])
im_b = np.empty([len(ind1),len(ind2)])
a = np.empty([len(ind1),len(ind2)])
im2 = np.zeros_like(im)
for i in ind1:
    for k in ind2:
        im_l[i,k] = int(im_lab[i,k,0])
        im_a[i,k] = int(im_lab[i,k,1])
        im_b[i,k] = int(im_lab[i,k,2])
        if im_a[i,k]<110 or im_a[i,k]>170:
            im2[i,k,:] = [255,255,255]
        else:
            im2[i,k,:] = [0,0,0]

#Filter noise, draw contour from canny edge detection
kernel = np.ones((3,3),np.uint8)
im2 = cv2.dilate(im2,None,iterations=2)
im2 = cv2.erode(im2,None,iterations=2)
im2_canny = cv2.Canny(im2,40,55)
im2_canny = cv2.dilate(im2_canny,None,iterations=1)
im2_contours,contours,hierarchy = cv2.findContours(im2_canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(im2_contours,contours,-1,(255,255,255),-1)

#Find pixel amounts for each contour
pre_areas = []
contours2 = []
im3_contours = np.zeros_like(im)
cim3 = np.zeros_like(im)
for i in range(len(contours)):
    pre_areas.append(cv2.contourArea(contours[i]))
    if pre_areas[i] > 50000:
        contours2.append(contours[i])
        cv2.drawContours(im3_contours,contours,i,(0,255,0),-1)

#Find the percentage of pixels of total image that belong to the plant canopy
plant_areas_pixels = []
for i in range(len(contours2)):
    plant_areas_pixels.append(cv2.contourArea(contours2[i]))

image_pixels = im.shape[0]*im.shape[1]
data = plant_areas_pixels[0]/image_pixels

plt.imshow(im3_contours,'gray')
plt.xticks([])
plt.yticks([])
plt.show()
print('Percentage of screen taken up:')
print(data)
