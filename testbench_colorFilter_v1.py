# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

#greenLower = (29, 86, 6);
#greenUpper = (64, 255, 255);
greenLower = (50, 100, 100);
greenUpper = (70, 255, 255);

pts = deque(maxlen=64);

img = cv2.imread('teste_1.jpg',1);

blurred = cv2.GaussianBlur(img, (11, 11), 0); #reduce high frequency noise
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);

# construct a mask for the color "green", then perform
# a series of dilations and erosions to remove any small
# blobs left in the mask
mask = cv2.inRange(hsv, greenLower, greenUpper);
mask = cv2.erode(mask, None, iterations=2);
mask = cv2.dilate(mask, None, iterations=2);

# find contours in the mask and initialize the current
# (x, y) center of the ball
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,	cv2.CHAIN_APPROX_SIMPLE)[-2];
center = None;

# only proceed if at least one contour was found
if len(cnts) > 0:
	# find the largest contour in the mask, then use
	# it to compute the minimum enclosing circle and
	# centroid
    c = max(cnts, key=cv2.contourArea);
    ((x, y), radius) = cv2.minEnclosingCircle(c);
	#print ((x,y));
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

	# only proceed if the radius meets a minimum size
    if (radius > 100) and (radius < 300):
        print "aquii";
		# draw the circle and centroid on the frame,
		# then update the list of tracked points
		#cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 255), 2);
        cv2.circle(img, (int(x), int(y)), int(radius),(0, 0, 0), 1);
        print radius;
        cv2.circle(img, center, 5, (0, 0, 0), 1);


# show the frame to our screen
cv2.imshow("Image", img);
cv2.imshow("Mask", mask);
key = cv2.waitKey(0);

# cleanup the camera and close any open windows

cv2.destroyAllWindows();
