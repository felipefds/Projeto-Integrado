import cv2

img = cv2.imread('psita.jpg',1);

cv2.namedWindow('Title', cv2.WINDOW_NORMAL);
"""
There is a special case where you can already create a window and load image to it later. In that case, you can specify whether window is resizable or not. It is done with the function cv2.namedWindow(). By default, the flag is cv2.WINDOW_AUTOSIZE. But if you specify flag to be cv2.WINDOW_NORMAL, you can resize window. It will be helpful when image is too large in dimension and adding track bar to windows.
"""

cv2.imshow('Title',img);
cv2.waitKey(0);
cv2.destroyAllWindows();
