import numpy as np
from numpy import matrix
import cv2
import matplotlib.pyplot as plt

###This program will find the areas and perimeters for all plant canponies in a single image
###This program will use RGB coloration analysis in the RGB color space to differentiate between plant canopies, reference square, and background
###Note - the plant canopy areas must all be larger than the 1 square inch reference 

image = r'' #insert image directory here
im = cv2.imread(image)
ind1 = list(range(im.shape[0]))
ind2 = list(range(im.shape[1]))
ref_pixel = cv2.inRange(im,np.array([220,110,30]),np.array([260,180,80])) #Find pixels for reference square
im_sub = np.empty([len(ind1),len(ind2)])
im2 = cv2.imread(image) #Initialize new image
for i in ind1:
    for k in ind2:
        im_sub[i,k] = int(im[i,k,1])/(int(im[i,k,0])+int(im[i,k,1])+int(im[i,k,2])+1) #Coloration analysis parameters
        if ((im_sub[i,k]>0.3 and im[i,k,0]>90) or (int(im[i,k,0])-int(im[i,k,2]))>85):
            im2[i,k,:] = [0,0,0] #Make background white pixels
        else:
            im2[i,k,:] = [255,255,255] #Make plant canopies black pixels
for i in ind1:
    for k in ind2:
        if ref_pixel[i,k] == 255:
            im2[i,k,:] = [255,255,255] #Make reference square black pixels

edged = cv2.Canny(im2,40,55)
edged = cv2.dilate(edged,None,iterations=1)
edged = cv2.erode(edged,None,iterations=1)
im3,contours,hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(im2,contours,-1,(255,255,255),1)

#Find preliminary areas of all contours, concatenate into a list
#Isolate areas above a range, sort them based on size
#This will give preliminary areas for reference square and for each plant
pre_areas = []
cim = np.zeros_like(im2)
for i in range(len(contours)):
    pre_areas.append(cv2.contourArea(contours[i]))
    if pre_areas[i] > 1000:
        cv2.drawContours(cim,contours,i,(255,255,255),-1)

#Filter out noise in the found countour areas
#Again find the image contours
#Find the new (final) contour areas
kernel = np.ones((3,3),np.uint8)
cim2 = cv2.erode(cim,kernel,iterations=2)
cim2 = cv2.dilate(cim2,kernel,iterations=2)
cim2 = cv2.Canny(cim2,40,55)
im2,contours,hierarchy = cv2.findContours(cim2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cim2,contours,-1,(255,255,255),3)

#Create arrays of areas and perimeters
final_areas = []
final_perimeters = []
for i in range(len(contours)):
    final_areas.append(cv2.contourArea(contours[i]))
    final_perimeters.append(cv2.arcLength(contours[i],True))

#Create 2D array of the area,perimeter pairs, except for the reference
#The reference is used to find the actual area and perimeter (in^2,in)
data = []
for i in range(len(contours)):
    if final_areas[i]>min(final_areas) and final_perimeters[i]>min(final_perimeters):
        new_area = final_areas[i]/min(final_areas)
        new_peri = final_perimeters[i]/min(final_perimeters)*4
        data.append([format(new_area,'.3f'),format(new_peri,'.3f')])

#Print out data, image showing contours
plt.imshow(cim2,'gray')
plt.show()
print('Area, Perimeter Pairs:')
print(data)
