#include <Servo.h>

#define PIN_SERVO_NORTE  8
#define PIN_SERVO_LESTE  9
#define PIN_SERVO_SUL    10
#define PIN_SERVO_OESTE  11

Servo s_norte;
Servo s_leste;
Servo s_sul;
Servo s_oeste;

void setup()
{
  s_norte.attach(PIN_SERVO_NORTE);
  s_leste.attach(PIN_SERVO_LESTE);
  s_sul.attach(PIN_SERVO_SUL);
  s_oeste.attach(PIN_SERVO_OESTE);
        
  Serial.begin(9600);
  
  s_norte.write(45);
  s_leste.write(45);
  s_sul.write(45);
  s_oeste.write(45);

  
}

void loop(){
  
}

