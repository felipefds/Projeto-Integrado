import cv2
import numpy as np

"""
This is a common question found in stackoverflow.com. It is very
simple and you can use the same function, cv2.cvtColor(). Instead
of passing an image, you just pass the BGR values you want. For example,
to find the HSV value of Green, try following commands in Python terminal:"""

green = np.uint8([[[0,255,0 ]]]);
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV);

print (hsv_green);

"""Now you take [H-10, 100,100] and [H+10, 255, 255] as lower bound and upper
bound respectively."""
