import numpy as np
from numpy import matrix
import cv2
import matplotlib.pyplot as plt

###This program will find the areas and perimeters of all plant canopies in a single image
###This program uses LAB color space coloration analysis to differentiate between plant canopy, reference square, and background
###For this program, the reference square area must be smaller than all of the plant canopy areas

image = r'' #Insert image directory
im = cv2.imread(image)
im_lab = cv2.cvtColor(im,cv2.COLOR_BGR2LAB) #Put image into LAB color space
im_lab = cv2.GaussianBlur(im_lab,(5,5),0)

#LAB coloration analysis
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
        elif im_a[i,k]<120 and im_l[i,k]<120:
            im2[i,k,:] = [255,255,255]
        else:
            im2[i,k,:] = [0,0,0]

#Canny edge detection
kernel = np.ones((3,3),np.uint8)
im2 = cv2.dilate(im2,None,iterations=2)
im2 = cv2.erode(im2,None,iterations=2)
im2_canny = cv2.Canny(im2,40,55)
im2_canny = cv2.dilate(im2_canny,None,iterations=1)
im2_contours,contours,hierarchy = cv2.findContours(im2_canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(im2_contours,contours,-1,(255,255,255),-1)

#Drawing contours
pre_areas = []
contours2 = []
im3_contours = np.zeros_like(im)
cim3 = np.zeros_like(im)
for i in range(len(contours)):
    pre_areas.append(cv2.contourArea(contours[i]))
    if pre_areas[i] > 5000:
        contours2.append(contours[i])
        cv2.drawContours(im3_contours,contours,i,(0,255,0),-1)

#Finding plant canopy area and perimeter pixel values
plant_areas_pixels = []
plant_perimeters_pixels = []
for i in range(len(contours2)):
    plant_areas_pixels.append(cv2.contourArea(contours2[i]))
    plant_perimeters_pixels.append(cv2.arcLength(contours2[i],True))
plant_areas_pixels.sort()
plant_perimeters_pixels.sort()

#Calculating plant canopy areas and perimeters
plant_areas = []
plant_perimeters = []
for i in range(len(plant_areas_pixels)):
    plant_areas.append(plant_areas_pixels[i]/plant_areas_pixels[0])
    plant_perimeters.append(plant_perimeters_pixels[i]/plant_perimeters_pixels[0])
plant_areas = plant_areas[1:len(plant_areas)]
plant_perimeters = plant_perimeters[1:len(plant_perimeters)]

data = []
for i in range(len(plant_areas)):
        data.append([format(plant_areas[i],'.3f'),format(plant_perimeters[i],'.3f')])

plt.imshow(im3_contours,'gray')
plt.xticks([])
plt.yticks([])
plt.show()
print('Area, Perimeter Pairs:')
print(data)
