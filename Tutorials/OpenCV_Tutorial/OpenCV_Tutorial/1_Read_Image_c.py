import cv2
from matplotlib import pyplot as plt

img = cv2.imread('psita.jpg',1);

"""
Color image loaded by OpenCV is in BGR mode. But Matplotlib displays in RGB mode. So color images will not be displayed correctly in Matplotlib if image is read with OpenCV. Please see the exercises for more details.
"""
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic');
plt.xticks([]), plt.yticks([]);  # to hide tick values on X and Y axis
plt.show();
