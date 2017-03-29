import cv2
import cv2.cv as cv
import numpy as np

img = cv2.imread('olympics.png',0);
img = cv2.medianBlur(img,5);
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR);

circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0);

circles = np.uint16(np.around(circles));
for i in circles[0,:]:
    #i[0] = x_center
    #i[1] = y_center
    #i[2] = circle_radius
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2) #cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    print ("Center: " + str(i[0]) + "," + str(i[1]));

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
