import cv2

print ("Color conversion flags: ");

flags = [i for i in dir(cv2) if i.startswith('COLOR_')];

print (flags);
