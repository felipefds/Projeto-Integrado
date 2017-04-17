import sys
import math
import serial
import time

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

serialPorts = ['/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3',
            'COM1','COM2','COM3','COM4'];

def GetSerialPort():
    for port in serialPorts:
        try:
            # Iniciando conexao serial
            comport = serial.Serial(port, 9600, timeout = 1);
            time.sleep(1.8); # Entre 1.5s a 2s
            if (comport.isOpen() == True):
                print "Port to be used: " + port;
                comport.flush();
                comport.close();
                return port;
        except:
            pass;

    return "0";

def SendTextToPort(text,port):

    print "SendTextToPort(): Text to be sent - " + text;

    if (port == "0"):
        print "SendTextToPort(): No microcontrollers connected";

    else:
        comport = serial.Serial(port, 9600, timeout = 1);
        comport.flush();

        # Time entre a conexao serial e o tempo para escrever (enviar algo)
        #time.sleep(1.5); # Entre 1.5s a 2s

        for i in range (len(text)):
            comport.write(text[i].encode());
            time.sleep(2);
        #comport.write(PARAM_ASCII)

        VALUE_SERIAL=comport.readline();
        print 'SendTextToPort(): Serial port return - %s' % (VALUE_SERIAL);

        # Fechando conexao serial
        comport.close();

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

print 'Ball position: [' + sys.argv[1] + ';' + sys.argv[2] + ']';

xTarget = int (sys.argv[1]);
yTarget = int (sys.argv[2]);

# def GetMicAngle (xTarget, yTarget, wing, xMic, yMic):
northMic.angle = GetMicAngle (xTarget, yTarget, northMic.wing, northMic.x, northMic.y);
eastMic.angle = GetMicAngle (xTarget, yTarget, eastMic.wing, eastMic.x, eastMic.y);
southMic.angle = GetMicAngle (xTarget, yTarget, southMic.wing, southMic.x, southMic.y);
westMic.angle = GetMicAngle (xTarget, yTarget, westMic.wing, westMic.x, westMic.y);

text = str(northMic.angle) + ';' + str(eastMic.angle) + ';' + str(southMic.angle) + ';' + str(westMic.angle) + ';';

#CheckPorts();
port = GetSerialPort();
SendTextToPort(text,port);

"""print ("North mic angle: " + str(northMic.angle));
print ("East mic angle: " + str(eastMic.angle));
print ("South mic angle: " + str(southMic.angle));
print ("West mic angle: " + str(westMic.angle));
"""
