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
            print 'SendTextToPort(): Serial port return - %s' % (VALUE_SERIAL);
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

print 'Arguments: ['+sys.argv[1]+';'+sys.argv[2]+']'+',['+sys.argv[3]+';'+sys.argv[4]+']'+',['+sys.argv[5]+';'+sys.argv[6]+']';

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 1st ball position
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

print ("#1");
print 'Ball position: ['+sys.argv[1]+';'+sys.argv[2]+']';

time_one = time.time(); # Initializes clock
SendTextToPort(text,port);
WaitNextString(port);
time_two = time.time(); # Finishes clock
interval = time_two-time_one; # Calculates elapsed time
print ("Intervalo de tempo: " + str(interval));

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 2nd ball position
xTarget = int (sys.argv[3]);
yTarget = int (sys.argv[4]);

# def GetMicAngle (xTarget, yTarget, wing, xMic, yMic):
northMic.angle = GetMicAngle (xTarget, yTarget, northMic.wing, northMic.x, northMic.y);
eastMic.angle = GetMicAngle (xTarget, yTarget, eastMic.wing, eastMic.x, eastMic.y);
southMic.angle = GetMicAngle (xTarget, yTarget, southMic.wing, southMic.x, southMic.y);
westMic.angle = GetMicAngle (xTarget, yTarget, westMic.wing, westMic.x, westMic.y);

text = str(northMic.angle) + ';' + str(eastMic.angle) + ';' + str(southMic.angle) + ';' + str(westMic.angle) + ';';

#CheckPorts();
#port = GetSerialPort();

print ("#2");
print 'Ball position: ['+sys.argv[3]+';'+sys.argv[4]+']';

time_one = time.time(); # Initializes clock
SendTextToPort(text,port);
WaitNextString(port);
time_two = time.time(); # Finishes clock
interval = time_two-time_one; # Calculates elapsed time
print ("Intervalo de tempo: " + str(interval));

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 3rd ball position
xTarget = int (sys.argv[5]);
yTarget = int (sys.argv[6]);

# def GetMicAngle (xTarget, yTarget, wing, xMic, yMic):
northMic.angle = GetMicAngle (xTarget, yTarget, northMic.wing, northMic.x, northMic.y);
eastMic.angle = GetMicAngle (xTarget, yTarget, eastMic.wing, eastMic.x, eastMic.y);
southMic.angle = GetMicAngle (xTarget, yTarget, southMic.wing, southMic.x, southMic.y);
westMic.angle = GetMicAngle (xTarget, yTarget, westMic.wing, westMic.x, westMic.y);

text = str(northMic.angle) + ';' + str(eastMic.angle) + ';' + str(southMic.angle) + ';' + str(westMic.angle) + ';';

#CheckPorts();
#port = GetSerialPort();

print ("#3");
print 'Ball position: ['+sys.argv[5]+';'+sys.argv[6]+']';

time_one = time.time(); # Initializes clock
SendTextToPort(text,port);
WaitNextString(port);
time_two = time.time(); # Finishes clock
interval = time_two-time_one; # Calculates elapsed time
print ("Intervalo de tempo: " + str(interval));
