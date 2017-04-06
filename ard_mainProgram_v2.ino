#include <string.h>
#include <stdlib.h>
//#include <Servo.h>

#define MAX_CARACTERS    100
#define MAX_ORDEM_ANGULO 3

unsigned count = 0;
unsigned positionMic = 1;
//Servo s;

char name [MAX_CARACTERS];
char anguloNorte [MAX_ORDEM_ANGULO];
char anguloLeste [MAX_ORDEM_ANGULO];
char anguloSul [MAX_ORDEM_ANGULO];
char anguloOeste [MAX_ORDEM_ANGULO];

void setup()
{
 //s.attach(SERVO);
 Serial.begin(9600);
 //s.write(0);
}

void loop() { 

  while (Serial.available() > 0) {
    name[count] = Serial.read();

    if (name[count] != ';'){
      if (positionMic == 1){
        anguloNorte[count] = Serial.read();
        count++;
      }
      if (positionMic == 2){
        anguloLeste[count] = Serial.read();
        count++;
      }
      if (positionMic == 3){
        anguloSul[count] = Serial.read();
        count++;
      }
      if (positionMic == 4){
        anguloOeste[count] = Serial.read();
        count++;
      }
    } else {
      positionMic++;
      count = 0;
    }
  } //Fim da Leitura Serial
  s.write(strtol(anguloNorte));
  s.write(strtol(anguloLeste));
  s.write(strtol(anguloSul));
  s.write(strtol(anguloOeste));
} //Fim do loop
