import cv2
import numpy as np

#Reading the image
img = cv2.imread('img-bola.jpeg',1);

#reduce high frequency noise
img_blurred = cv2.GaussianBlur(img, (11, 11), 0);

#Converting to HSV color space
hsv_img = cv2.cvtColor(img_blurred, cv2.COLOR_BGR2HSV);

#Defining color range for filter
lower_green = (29,86,6);
upper_green = (64,255,255);

# Threshold the HSV image to get only green colors
mask = cv2.inRange(hsv_img, lower_green, upper_green); #cv2.inRange(image,lower,upper)
mask = cv2.erode(mask, None, iterations=2);
mask = cv2.dilate(mask, None, iterations=2);

cv2.imshow('Filtro',mask);
cv2.imshow('Imagem original da Bola em RGB',img);
cv2.imshow('Imagem original da Bola Blurred',img_blurred);
cv2.imshow('Imagem original da Bola em HSV',hsv_img);
cv2.waitKey(0);
cv2.destroyAllWindows();
