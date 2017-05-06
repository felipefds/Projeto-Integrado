import cv2

events = [i for i in dir(cv2) if 'EVENT' in i];

print ("List of events in CV2 library:");
print (events);
