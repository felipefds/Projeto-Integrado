# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

#Blue_1 in HSV
blueLower = (104, 66, 127);
blueUpper = (152, 196, 255);

#Blue_2 in HSV
#blueLower = (113, 88, 245);
#blueUpper = (255, 255, 122);

pts = deque(maxlen=64)

camera = cv2.VideoCapture(1)

# keep looping
while True:
	# grab the current frame
    (grabbed, frame) = camera.read()
		#grabbed == boolean

	# resize the frame, blur it, and convert it to the HSV
	# color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0) #reduce high frequency noise
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask = cv2.inRange(hsv, blueLower, blueUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        #c = max(cnts, key=cv2.contourArea)

        cnts_array = [];

        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c);
            cnts_array.append((x,y));

            M = cv2.moments(c);
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    		# only proceed if the radius meets a minimum size
            if radius > 10:
    			# draw the circle and centroid on the frame,
    			# then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2);
                cv2.circle(frame, center, 5, (0, 0, 255), -1);


    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break;

    # Getting Microphones Positions -------------------
    if key == ord("m"):
        print "Getting microphones positions..."
        (x_north, y_north) = (0,0);
        (x_east, y_east) = (0,0);
        (x_south, y_south) = (0,0);
        (x_west, y_west) = (0,0);

        #Get frame size (heigth and width)
        (frame_height, frame_width,_) = frame.shape; #frame.shape(height, width, channels)

        # Separating microphones
        for (x,y) in cnts_array:
            if ( ((0.5-0.25)*frame_width < x) and (x < (0.5+0.25)*frame_width) and (y < 0.25*frame_height)):
                if (x_north,y_north) == (0,0):
                    (x_north,y_north) = (x,y);
                else:
                    (x_north,y_north) = ( 0.5*(x+x_north), 0.5*(y+y_north));

            if ( ((0.5-0.25)*frame_width < x) and (x < (0.5+0.25)*frame_width) and (0.75*frame_height < y)):
                if (x_south,y_south) == (0,0):
                    (x_south,y_south) = (x,y);
                else:
                    (x_south,y_north) = ( 0.5*(x+x_south), 0.5*(y+y_south));

            if ( ((0.5-0.25)*frame_height < y) and (y < (0.5+0.25)*frame_height) and (0.75*frame_width < x)):
                if (x_east,y_east) == (0,0):
                    (x_east,y_east) = (x,y);
                else:
                    (x_east,y_east) = ( 0.5*(x+x_east), 0.5*(y+y_east));

            if ( ((0.5-0.25)*frame_height < y) and (y < (0.5+0.25)*frame_height) and (x < 0.25*frame_width)):
                if (x_west,y_west) == (0,0):
                    (x_west,y_west) = (x,y);
                else:
                    (x_west,y_west) = ( 0.5*(x+x_west), 0.5*(y+y_west));

        print ("North: " + str((x_north,y_north)));
        print ("East: " + str((x_east,y_east)));
        print ("South: " + str((x_south,y_south)));
        print ("West: " + str((x_west,y_west)));

        print "Microphones positions saved."

    if key == ord("s"):
        print "Saving frame...";
        cv2.imwrite('findMic.png',frame);
        print "Frame Saved";
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
