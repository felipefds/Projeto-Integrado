import cv2
import cv2.cv as cv
import numpy as np

#image = cv2.imread("rainbow.jpg",1);

filename = 'tennis_ball_3.jpg'

original_image = cv2.imread(filename,1);
image = cv2.imread(filename,1);
image = cv2.medianBlur(image,5);


#define color boundaries in BGR
lower_green = [0, 100, 100];
upper_green = [70, 255, 255];

# define the list of boundaries
boundaries = [
	(lower_green, upper_green)
];

color = ["Green"];
count = 0;
font = cv2.FONT_HERSHEY_SIMPLEX;

# loop over the boundaries
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8"); #uint8 = unsigned int from 0 to 255
    upper = np.array(upper, dtype = "uint8");

	# find the colors within the specified boundaries and apply
	# the mask
    mask = cv2.inRange(image, lower, upper);
    output = cv2.bitwise_and(image, image, mask = mask);

    cv2.putText(output,color[count],(10,40), font, 1,(255,255,255),1)
    count = count+1;

    cv2.imwrite('output.jpg',output);
    gray_output = cv2.imread('output.jpg',0);

    cimg = cv2.cvtColor(gray_output,cv2.COLOR_GRAY2BGR);
    circles = cv2.HoughCircles(gray_output,cv.CV_HOUGH_GRADIENT,50,20,
                                param1=10,param2=50,minRadius=0,maxRadius=0);

    circles = np.uint16(np.around(circles));
    for i in circles[0,:]:
        #i[0] = x_center
        #i[1] = y_center
        #i[2] = circle_radius
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2) #cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        print ("Center: " + str(i[0]) + "," + str(i[1]) + ", Radius: " + str(i[2]));

	# show the images
    #cv2.imshow("Gray Image", gray_output)
    cv2.imshow("Gray Image", cimg)
    cv2.imshow("Original Image", original_image)
    cv2.waitKey(0);

cv2.destroyAllWindows();
