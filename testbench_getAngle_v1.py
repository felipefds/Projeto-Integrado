import sys
import math

class Mic(object):
    def __init__(self, wing, x, y):
        self.wing = wing.upper();
        self.x = x;
        self.y = y;

    angle = 0;

northMic = Mic ('North', 0, 100);
eastMic = Mic ('East', 100, 0);
southMic = Mic ('South', 0, -100);
westMic = Mic ('West', -100, 0);

def GetMicAngle (xTarget, yTarget, wing, xMic, yMic):

    if (wing == "SOUTH"):
        if (xTarget == xMic):
            return 90;
        elif (xTarget > xMic):
            return math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
        else:
            return 180-math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));

    elif (wing == "NORTH"):
        if (xTarget == xMic):
            return 90;
        elif (xTarget > xMic):
            return 180-math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
        else:
            return math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));

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

print 'Ball position: [' + sys.argv[1] + ';' + sys.argv[2] + ']';

xTarget = int (sys.argv[1]);
yTarget = int (sys.argv[2]);

# def GetMicAngle (xTarget, yTarget, wing, xMic, yMic):
northMic.angle = GetMicAngle (xTarget, yTarget, northMic.wing, northMic.x, northMic.y);
eastMic.angle = GetMicAngle (xTarget, yTarget, eastMic.wing, eastMic.x, eastMic.y);
southMic.angle = GetMicAngle (xTarget, yTarget, southMic.wing, southMic.x, southMic.y);
westMic.angle = GetMicAngle (xTarget, yTarget, westMic.wing, westMic.x, westMic.y);

print ("North mic angle: " + str(northMic.angle));
print ("East mic angle: " + str(eastMic.angle));
print ("South mic angle: " + str(southMic.angle));
print ("West mic angle: " + str(westMic.angle));
