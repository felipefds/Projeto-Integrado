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
        print "SendTextToPort(): No microcontrollers connected.";

    else:
        comport = serial.Serial(port, 9600, timeout = 1);
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
        comport.close();

def WaitNextString(port):
    # Wait for arduino to send a '.' character, indicating he can receive next ball position
    if (port == "0"):
        print "WaitNextString(): No microcontrollers connected."
    else:
        comport = serial.Serial(port, 9600, timeout = 1);
        VALUE_SERIAL=comport.read();
        while (VALUE_SERIAL != '.'):
            VALUE_SERIAL=comport.read();
            print ('SendTextToPort(): Serial port return - %s' % (VALUE_SERIAL));
            time.sleep(0.5);

        #Fechando conexao Serial
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


print ('#Args:' + str(len(sys.argv))s);

if ((len(sys.argv) % 2 == 0) or (len(sys.argv) == 1)):
    print ("Error: Please type an odd number.");
    exit(0);

tuplesCounter = 0;
positionsList = [];
xTarget = yTarget = 0;

for arg in range(1,len(sys.argv)):
    #print sys.argv[arg];
    if (arg % 2 == 1):
        xTarget = int(sys.argv[arg]);
    if (arg % 2 == 0):
        yTarget = int(sys.argv[arg]);
        positionsList.append((xTarget,yTarget));
        #print (positionsList[tuplesCounter]);
        tuplesCounter+=1;

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#CheckPorts();
port = GetSerialPort();

if (port == "0"):
    print ("No microcontrollers connected.");

tuplesCounter = 1;

for (xTarget,yTarget) in positionsList:
    # def GetMicAngle (xTarget, yTarget, wing, xMic, yMic):
    northMic.angle = GetMicAngle (xTarget, yTarget, northMic.wing, northMic.x, northMic.y);
    eastMic.angle = GetMicAngle (xTarget, yTarget, eastMic.wing, eastMic.x, eastMic.y);
    southMic.angle = GetMicAngle (xTarget, yTarget, southMic.wing, southMic.x, southMic.y);
    westMic.angle = GetMicAngle (xTarget, yTarget, westMic.wing, westMic.x, westMic.y);

    text = str(northMic.angle) + ';' + str(eastMic.angle) + ';' + str(southMic.angle) + ';' + str(westMic.angle) + ';';

    print ('#'+str(tuplesCounter)+ ' Ball position: ['+str(xTarget)+';'+str(yTarget)+']'+' - ' + text);

    if (port != "0"):
        time_one = time.time(); # Initializes clock
        SendTextToPort(text,port);
        WaitNextString(port);
        time_two = time.time(); # Finishes clock
        interval = time_two-time_one; # Calculates elapsed time
        print ("Time Interval: " + str(interval));

    tuplesCounter +=1;
