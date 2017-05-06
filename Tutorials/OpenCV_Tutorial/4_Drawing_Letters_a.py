import numpy as np
import cv2

# Create a black image
img = np.zeros((512,512,3), np.uint8);

"""
To put texts in images, you need specify following things.

        Text data that you want to write
        Position coordinates of where you want put it (i.e. bottom-left corner where data starts).
        Font type (Check cv2.putText() docs for supported fonts)
        Font Scale (specifies the size of font)
        regular things like color, thickness, lineType etc. For better look, lineType = cv2.LINE_AA is recommended.
"""


# Draw a diagonal blue line with thickness of 5 px
font = cv2.FONT_HERSHEY_SIMPLEX;
cv2.putText(img,'OpenCV',(10,500), font, 1,(255,255,255),2,cv2.LINE_AA);

cv2.imshow('Title',img);
cv2.waitKey(0);
cv2.destroyAllWindows();
