import cv2
import cv2.cv as cv
import numpy as np

filename = 'moon.jpg'

img = cv2.imread(filename,1);
img = cv2.medianBlur(img,5);
img2 = cv2.imread(filename,0);
cimg = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR);

circles = cv2.HoughCircles(img2,cv.CV_HOUGH_GRADIENT,50,20,
                            param1=10,param2=50,minRadius=0,maxRadius=int(10));

"""
- cv2.HoughCircles(image, method, dp, minDist)
image: 8 bit single channel image. If working with a colored image, convert
to grayscale first.
- method: Defines the method to detect circles in images. Currently, the only
implemented method is cv2.HOUGH_GRADIENT
- minDist: Minimum distance between the center (x, y) coordinates of detected
circles. If the minDist is too small, multiple circles in the same neighborhood
as the original may be (falsely) detected. If the minDist is too large, then some
circles may not be detected at all.
- param1: Gradient value used to handle edge detection in the Yuen et al. method.
- param2: Accumulator threshold value for the cv2.HOUGH_GRADIENT method. The smaller the threshold is, the more circles will be detected (including false circles). The larger the threshold is, the more circles will potentially be returned.
minRadius: Minimum size of the radius (in pixels).
maxRadius: Maximum size of the radius (in pixels).

"""

circles = np.uint16(np.around(circles));
for i in circles[0,:]:
    #i[0] = x_center
    #i[1] = y_center
    #i[2] = circle_radius
    # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2) #cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
    # draw the center of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
    print ("Center: " + str(i[0]) + "," + str(i[1]) + ", Radius: " + str(i[2]));

cv2.imshow('detected circles',img)
cv2.waitKey(0)
