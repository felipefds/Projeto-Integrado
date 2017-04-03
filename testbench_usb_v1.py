import serial

serialPorts = ['/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3',
            'COM1','COM2','COM3','COM4'];

text = "N45;L8;S130;O70"

def GetSerialPort():
    for port in serialPorts:
        try:
            # Iniciando conexao serial
            comport = serial.Serial(port, 9600, timeout = 1);
            #time.sleep(1.8); # Entre 1.5s a 2s
            if (comport.isOpen() == True):
                print "Port to be used: " + port;
                comport.flush();
                comport.close();
                return port;
        except:
            pass;

    return "0";

def SendTextToPort(port):

    print "SendTextToPort(): Text to be sent - " + text;

    if (port == "0"):
        print "SendTextToPort(): No microcontrollers connected"

    else:
        comport = serial.Serial(port, 9600, timeout = 1);
        comport.flush();

        # Time entre a conexao serial e o tempo para escrever (enviar algo)
        time.sleep(1.8) # Entre 1.5s a 2s

        for i in range (len(text)):
            comport.write(text[i].encode());
        #comport.write(PARAM_ASCII)

        VALUE_SERIAL=comport.readline()

        print '\nSendTextToPort(): Retorno da serial - %s' % (VALUE_SERIAL)

        # Fechando conexao serial
        comport.close();

print ("Inicio:");
#CheckPorts();
port = GetSerialPort();
try:
    SendTextToPort(port);
except:
    port = GetSerialPort();
    try:
        SendTextToPort(port);
    except:
        print("Connection Error.");
