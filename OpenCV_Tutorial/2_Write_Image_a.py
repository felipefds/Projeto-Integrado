import cv2

img = cv2.imread('psita.jpg',0);

cv2.imwrite('psita-gray.jpg',img);
#First argument is the file name, second argument is the image you want to save.

print ("Gray version of the picture saved.");
