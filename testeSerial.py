import serial
import time

while (1 > 0):
  comport = serial.Serial('COM3', 9600, timeout = 1);
  time.sleep(1.5);
  if (comport.isOpen() == True):
    comport.flush();
    comport.write("H");
    time.sleep(2);
    comport.close();