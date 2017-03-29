import cv2
import numpy as np
from matplotlib import pyplot as plt

#img = cv2.imread('grayscale.jpg');
img = cv2.imread('blue-image.jpg',0);
ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

# cv2.threshold(1,2,3,4)
#1 - Image source, which SHOULD BE grayscale image
#2 - Threshold Value
#3 - Maximum Value
#4 - Style of Thresholding (cv2.THRESH_TOZERO, cv2.THRESH_TRUNC, etc.)

ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in xrange(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()
