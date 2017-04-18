import cv2

img = cv2.imread('psita.jpg',1);
#img = cv2.imread('psita.jpg',cv2.IMREAD_GRAYSCALE);
#2nd argument:
#  (1)  cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
#  (0)  cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
#  (-1) cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel

cv2.imshow('Title',img);
cv2.waitKey(0);
cv2.destroyAllWindows();
