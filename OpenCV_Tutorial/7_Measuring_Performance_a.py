import cv2

img1 = cv2.imread('psita.jpg',1);

e1 = cv2.getTickCount();
"""cv2.getTickCount function returns the number of clock-cycles
after a reference event (like the moment machine was switched ON)
to the moment this function is called. So if you call it before
and after the function execution, you get number of clock-cycles
used to execute a function."""

cv2.imshow('Title 2',img1);

for i in xrange(5,49,2):
    img1 = cv2.medianBlur(img1,i);

e2 = cv2.getTickCount();

"""cv2.getTickFrequency function returns the frequency of clock-cycles,
or the number of clock-cycles per second.So to find the time of
execution in seconds, you can do following:"""

t = (e2 - e1)/cv2.getTickFrequency();
print t;

cv2.imshow('Title 1',img1);
cv2.waitKey(0);
cv2.destroyAllWindows();


# Result I got is 0.521107655 seconds
