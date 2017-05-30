# import the necessary packages
from collections import deque
import numpy as np
import imutils
import math
import serial
import time
import cv2

# Field Settings --------------------

class Mic(object):
    def __init__(self, wing, x, y):
        self.wing = wing.upper();
        self.x = x;
        self.y = y;

    angle = 0;

def GetMicAngle (xTarget, yTarget, wing, xMic, yMic):

    if (wing == "SOUTH"):
        if (xTarget == xMic):
            return 90;
        elif (xTarget > xMic):
            angle = math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            return math.trunc(angle);
        else:
            angle = 180-math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            return math.trunc(angle);

    elif (wing == "NORTH"):
        if (xTarget == xMic):
            return 90;
        elif (xTarget > xMic):
            angle = 180-math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            return math.trunc(angle);
        else:
            angle = math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            return math.trunc(angle);

    elif (wing == "EAST"):
        if (yTarget == yMic):
            return 90;
        angle = 180-GetMicAngle (yTarget, xTarget, "NORTH", yMic, xMic);
        return angle;

    elif (wing == "WEST"):
        if (yTarget == yMic):
            return 90;
        angle = GetMicAngle (yTarget, xTarget, "NORTH", yMic, xMic);
        return angle;

    else:
        return "Error";

#Initializing Mics Objects
northMic = Mic ('North', 0, 0);
eastMic = Mic ('East', 0, 0);
southMic = Mic ('South', 0, 0);
westMic = Mic ('West', 0, 0);

micPositionSet = False; #change to True when they are set for the 1st time

# define the lower and upper boundaries of the "Red"
# ball in the HSV color space, then initialize the
# list of tracked points
# Hint: use the "rangeDetector.py" program to set the color range

#Red_1 in HSV
redLower = (113, 88, 245);
redUpper = (255, 255, 255);
#Red_2 in HSV
#redLower = (113, 88, 245);
#redUpper = (255, 255, 122);

pts = deque(maxlen=64);

camera = cv2.VideoCapture(1);

# keep looping
while True:
	# grab the current frame
    (grabbed, frame) = camera.read();
		#grabbed == boolean

	# resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600);
    blurred = cv2.GaussianBlur(frame, (11, 11), 0); #reduce high frequency noise
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV);

	# construct a mask for the color "red", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask = cv2.inRange(hsv, redLower, redUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=6)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,	cv2.CHAIN_APPROX_SIMPLE)[-2];
    center = None;

    (x,y) = (0,0);
    text = "90;90;90;90";
    angleTextToDisplay = "No points to center. " + text;
    micTextToDisplay = "No microphones to center."

	# only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
	c = max(cnts, key=cv2.contourArea);
        ((x, y), radius) = cv2.minEnclosingCircle(c);

		# To print current ball position
		#print ((x,y));

        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
        if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2);
			cv2.circle(frame, center, 5, (0, 0, 255), -1);

		# Set Mic Angles
        if (micPositionSet != False):
            (xTarget,yTarget) = (x, y);
            northMic.angle = GetMicAngle (xTarget, yTarget, northMic.wing, northMic.x, northMic.y);
            eastMic.angle = GetMicAngle (xTarget, yTarget, eastMic.wing, eastMic.x, eastMic.y);
            southMic.angle = GetMicAngle (xTarget, yTarget, southMic.wing, southMic.x, southMic.y);
            westMic.angle = GetMicAngle (xTarget, yTarget, westMic.wing, westMic.x, westMic.y);

            text = str(northMic.angle) + ';' + str(eastMic.angle) + ';' + str(southMic.angle) + ';' + str(westMic.angle) + ';';
            angleTextToDisplay = "["+str(int(x))+";"+str(int(y))+"]"+ "  " + text;

            cv2.circle(frame, (int(northMic.x), int(northMic.y)), 20,(0, 255, 255), 2);
            cv2.circle(frame, (int(eastMic.x), int(eastMic.y)), 20,(0, 255, 255), 2);
            cv2.circle(frame, (int(southMic.x), int(southMic.y)), 20,(0, 255, 255), 2);
            cv2.circle(frame, (int(westMic.x), int(westMic.y)), 20,(0, 255, 255), 2);
			#cv2.circle(frame, center, 5, (0, 0, 255), -1);

            micTextToDisplay = "North: " + str(int(northMic.x)) + ";" + str(int(northMic.y));
            cv2.putText(frame,micTextToDisplay, (10,25), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1);
            micTextToDisplay = "East:  " + str(int(eastMic.x)) + ";" + str(int(eastMic.y));
            cv2.putText(frame,micTextToDisplay, (10,45), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1);
            micTextToDisplay = "South:  " + str(int(southMic.x)) + ";" + str(int(southMic.y));
            cv2.putText(frame,micTextToDisplay, (10,65), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1);
            micTextToDisplay = "West:  " + str(int(westMic.x)) + ";" + str(int(westMic.y));
            cv2.putText(frame,micTextToDisplay, (10,85), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1);

	# update the points queue
    pts.appendleft(center);


    for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
        if pts[i - 1] is None or pts[i] is None:
			continue;

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5);
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness);


    #cv2.putText(target, text, coordinates, font, font_size, text_color, text_thickness, type_of_line)
    cv2.putText(frame,angleTextToDisplay, (10,105), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1);

	# show the frame to our screen
    cv2.imshow("Frame", frame);
    cv2.imshow("Mask", mask);
    key = cv2.waitKey(1) & 0xFF;

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break;

    if key == ord("s"):
		print "Saving frame...";
		cv2.imwrite('finalPresentation.png',frame);
		print "Frame Saved";

    if key == ord("v"):
        print "Saving Video...";
        print "Video saved.";

    if key == ord("m"):
        print "Setting microphones positions...";
        blueLower = (104, 66, 127);
        blueUpper = (152, 196, 255);

        mask = cv2.inRange(hsv, blueLower, blueUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

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

        (northMic.x, northMic.y) = (x_north, y_north);
        (eastMic.x, eastMic.y) = (x_east, y_east);
        (southMic.x, southMic.y) = (x_south, y_south);
        (westMic.x, westMic.y) = (x_west, y_west);

        print ("North: " + str((northMic.x ,northMic.y)));
        print ("East: " + str((eastMic.x ,eastMic.y)));
        print ("South: " + str((southMic.x ,southMic.y)));
        print ("West: " + str((westMic.x ,westMic.y)));

        micPositionSet = True;

        print "Microphones positions set.";


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
