import cv2
import numpy as np

image = cv2.imread("rainbow.jpg",1);

#define color boundaries in BGR
lower_red = [17,15,100];
upper_red = [50,56,200];

lower_blue = [86,31,4];
upper_blue = [220,88,50];

lower_green = [50, 100, 100];
upper_green = [70, 255, 255];

lower_gray = [103, 86, 65];
upper_gray = [145, 133, 128];

# define the list of boundaries
boundaries = [
	(lower_red, upper_red),
	(lower_blue, upper_blue),
	(lower_green, upper_green),
	(lower_gray, upper_gray)
];

color = ["Red","Blue","Green","Gray"];
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

	# show the images
    cv2.imshow("Color Range", np.hstack([image, output]))
    cv2.waitKey(0);

cv2.destroyAllWindows();
