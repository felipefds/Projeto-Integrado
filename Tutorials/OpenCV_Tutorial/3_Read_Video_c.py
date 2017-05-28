import numpy as np
import cv2

for i in range(10):
    print i;
    cap = cv2.VideoCapture(i);
    print cap.isOpened();

"""To capture a video, you need to create a VideoCapture object. Its argument can be either the device index or the name of a video file.
Device index
is just the number to specify which camera. Normally one camera will be connected (as in my case). So I simply pass 0 (or
 -1). You can select the second camera by passing 1 and so on. """


# When everything done, release the capture
cap.release();
cv2.destroyAllWindows();
