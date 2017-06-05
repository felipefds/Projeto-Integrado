# import the necessary packages
from collections import deque
import numpy as np
import imutils
import math
import serial
import time
import cv2

# Initializing Variables
serialPorts = ['/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3',
            'COM1','COM2','COM3','COM4']; # For Windows and Ubuntu Operating Systems

class Mic(object):
    def __init__(self, wing, x, y):
        self.wing = wing.upper();
        self.x = x;
        self.y = y;
    angle = 0;

# Functions -------------
def GetSerialPort(): # Function to get the serial port to be used
    for port in serialPorts:
        try:
            # Iniciando conexao serial
            comport = serial.Serial(port, 9600, timeout = 1);
            time.sleep(1.8); # Entre 1.5s a 2s
            if (comport.isOpen() == True):
                print ("Port to be used: " + port);
                comport.flush();
                comport.close();
                return port;
        except:
            pass;

    return "0";

def SendTextToPort(text,port): # Function to send a text to the serial port

    print ("SendTextToPort(): Text to be sent - " + text);

    if (port == "0"):
        print ("SendTextToPort(): No microcontrollers connected.");

    else:
        #comport = serial.Serial(port, 9600, timeout = 1);
        comport.flush();

        # Time entre a conexao serial e o tempo para escrever (enviar algo)
        #time.sleep(1.5); # Entre 1.5s a 2s

        for i in range (len(text)):
            comport.write(text[i].encode());
            #time.sleep(2);
        #comport.write(PARAM_ASCII)

        #VALUE_SERIAL=comport.readline();
        #print 'SendTextToPort(): Serial port return - %s' % (VALUE_SERIAL);

        # Fechando conexao serial
        #comport.close();

def CheckNextStringAllowed(port): # Function to check if next ball position can be sent
    # Wait for arduino to send a '.' character, indicating he can receive next ball position
    if (port == "0"):
        print ("WaitNextString(): No microcontrollers connected.");
    else:
        #comport = serial.Serial(port, 9600, timeout = 1);
        VALUE_SERIAL=comport.read();
        #comport.close();
        if (VALUE_SERIAL == '.'):
            return True;

        return False;

def GetMicAngle (xTarget, yTarget, wing, xMic, yMic): # Function to calculate mic angle according to ball and mic position

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
        angle = GetMicAngle (yTarget, xTarget, "NORTH", yMic, xMic);
        return angle;

    elif (wing == "WEST"):
        if (yTarget == yMic):
            return 90;
        angle = 180-GetMicAngle (yTarget, xTarget, "NORTH", yMic, xMic);
        return angle;

    else:
        return "Error";

# Initializing Variables ------------
northMic = Mic ('North', 0, 0);
eastMic = Mic ('East', 0, 0);
southMic = Mic ('South', 0, 0);
westMic = Mic ('West', 0, 0);

# define the lower and upper boundaries of the "Red"
# ball in the HSV color space, then initialize the
# list of tracked points
# Hint: use the "rangeDetector.py" program to set the color range
redLower = (113, 88, 245); #Lower Red in HSV values for filter
redUpper = (255, 255, 255); #Upper Red in HSV values for filter

pts = deque(maxlen=64); # Points for ball red trail
camera = cv2.VideoCapture(0); # use cv2.VideoCapture(1) to use 2nd webcam
(xTarget, yTarget) = (0,0);
micPositionSet = False; # Change to True when they are set for the 1st time
savingVideo = False; # Change to True when video is being saved
videoFileCreated = False; #Change to True if video file is created for the 1st time
sendNextString = False; # Change to True if next string can be sent

port = GetSerialPort();
if (port != "0"):
    comport = serial.Serial(port, 9600, timeout = 1);

time_zero = time.time();
TIME_DELAY = 0.25; # If time.time() - time_zero > TIME_DELAY, string can be sent to serial port

# Main Loop
while True:
    (grabbed, frame) = camera.read(); # grab the current frame
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

    text = "90;90;90;90;"; # If mics positions are not set, all mics must turn 90 degrees
    angleTextToDisplay = "No points to center. " + text;
    micTextToDisplay = "No microphones to center."

	# Only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
	c = max(cnts, key=cv2.contourArea);
        ((xTarget, yTarget), radius) = cv2.minEnclosingCircle(c);
        (xTarget,yTarget) = (int(xTarget), int(yTarget));
		# To print current ball position
		# print ((xTarget,yTarget));

        M = cv2.moments(c);
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]));

		# Only proceed if the radius meets a minimum size
        if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (xTarget, yTarget), int(radius),(0, 255, 255), 2);
			cv2.circle(frame, center, 5, (0, 0, 255), -1);

		# Set Mic Angles
        if (micPositionSet == True):
            #(xTarget,yTarget) = (int(xTarget), int(yTarget));
            northMic.angle = GetMicAngle (xTarget, yTarget, northMic.wing, northMic.x, northMic.y);
            eastMic.angle = GetMicAngle (xTarget, yTarget, eastMic.wing, eastMic.x, eastMic.y);
            southMic.angle = GetMicAngle (xTarget, yTarget, southMic.wing, southMic.x, southMic.y);
            westMic.angle = GetMicAngle (xTarget, yTarget, westMic.wing, westMic.x, westMic.y);

            text = str(northMic.angle) + ';' + str(eastMic.angle) + ';' + str(southMic.angle) + ';' + str(westMic.angle) + ';';
            angleTextToDisplay = "["+str(int(xTarget))+"; "+str(int(yTarget))+"] " + text;

            # Sending text to serial port
            if (time.time() - time_zero > TIME_DELAY):
                time_zero = time.time(); # Reinitializes time_zero to current time
                if (port != "0"):
                    sendNextString = CheckNextStringAllowed(port); # Check if next string can be sent
                    if (sendNextString == True):
                        SendTextToPort(text,port);

            # Drawing Mics position circles
            cv2.circle(frame, (int(northMic.x), int(northMic.y)), 20,(0, 255, 255), 2);
            cv2.circle(frame, (int(eastMic.x), int(eastMic.y)), 20,(0, 255, 255), 2);
            cv2.circle(frame, (int(southMic.x), int(southMic.y)), 20,(0, 255, 255), 2);
            cv2.circle(frame, (int(westMic.x), int(westMic.y)), 20,(0, 255, 255), 2);
			#cv2.circle(frame, center, 5, (0, 0, 255), -1);

            # Displaying Mics coordinates in frame
            micTextToDisplay = "North: " + str(int(northMic.x)) + ";" + str(int(northMic.y));
            cv2.putText(frame,micTextToDisplay, (10,25), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1);
            micTextToDisplay = "East:  " + str(int(eastMic.x)) + ";" + str(int(eastMic.y));
            cv2.putText(frame,micTextToDisplay, (10,45), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1);
            micTextToDisplay = "South: " + str(int(southMic.x)) + ";" + str(int(southMic.y));
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
    #cv2.imshow("Mask", mask);

    key = cv2.waitKey(1) & 0xFF;

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"): # Quit Program
        break;

    if key == ord("h"):
        print ("Help:");
        print ("Press 'm' to get microphones positions;");
        print ("Press 'p' to check microcontrollers connected to serial ports;");
        print ("Press 's' to save current frame to a *png file;");
        print ("Press 'v' to start/stop recording frame video;")
        print ("\nPress 'q' to quit application.")

    if key == ord("p"): # Check for serial port
        port = GetSerialPort();
        if (port == "0"):
            print ("No microcontrollers connected.");
        else:
            print ("Port to be used: " + port);

    if key == ord("s"): # Save Frame to png file
		print ("Saving frame...");
		cv2.imwrite('finalPresentation.png',frame);
		print ("Frame Saved");

    if key == ord("m"): # Set Microphones Positions
        print ("Setting microphones positions...");
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
                ((xTarget, yTarget), radius) = cv2.minEnclosingCircle(c);
                cnts_array.append((xTarget,yTarget));

                M = cv2.moments(c);
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        		# only proceed if the radius meets a minimum size
                if radius > 10:
        			# draw the circle and centroid on the frame,
        			# then update the list of tracked points
                    cv2.circle(frame, (int(xTarget), int(yTarget)), int(radius),(0, 255, 255), 2);
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


    #Saving Video
    if ((videoFileCreated == False) and (savingVideo == True)):
        # Create video file
        (frame_height, frame_width,_) = frame.shape;
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter('teste.avi',fourcc, 30.0, (frame_width, frame_height))
        print "Video file created.";
        videoFileCreated = True;

    if (savingVideo == True):
        # Save frames to video file.
        out.write(frame);
        pass;

    if key == ord("v"):
        if savingVideo == False:
            print "Saving video...";
            savingVideo = True;

        else:
            print "Video saved.";
            #Release video file
            out.release();
            savingVideo = False;
            videoFileCreated = False;

# cleanup the camera and close any open windows
try:
    if out.isOpened():
        print ("out file released.");
        out.release();
except:
    pass;

try:
    if (comport.isOpened()):
        print ("comport file released.")
        comport.close();
except:
    pass;
camera.release();
print ("camera released.");
cv2.destroyAllWindows();
