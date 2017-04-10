#include <string.h>
#include <stdlib.h>
//#include <Servo.h>

#define MAX_CARACTERS    100
#define MAX_ORDEM_ANGULO 3

unsigned count = 0;
unsigned positionMic = 1;
//Servo s;

char anguloNorte [MAX_ORDEM_ANGULO];
char anguloLeste [MAX_ORDEM_ANGULO];
char anguloSul [MAX_ORDEM_ANGULO];
char anguloOeste [MAX_ORDEM_ANGULO];

void setup()
{
 //s.attach(SERVO);
 Serial.begin(9600);
 pinMode(13,OUTPUT); //para indicar que chegou no 4o angulo (OESTE)
 //s.write(0); 
}

char receivedChar;
char textoCompleto[MAX_CARACTERS];
int contador = 0;

void loop() { 
  contador = 0;
  
  while (Serial.available() > 0) {

    receivedChar = Serial.read();
    //name[count] = Serial.read();
    //name[count] = received[0];
    
    textoCompleto[contador] = receivedChar;
    contador++;

    /*
    A porta serial eh uma fila e a cada Serial.read()
    retiramos um caracter dessa fila. Entao, fazer 
      name[count] = Seral.read();
    e
      anguloNorte[count] = Serial.read();
    retira DOIS caracteres da fila.
    */

    if (receivedChar != ';'){
      if (positionMic == 1){
        //anguloNorte[count] = Serial.read();
        anguloNorte[count] = receivedChar;
        count++;
      }
      if (positionMic == 2){
        //anguloLeste[count] = Serial.read();
        anguloLeste[count] = receivedChar;
        count++;
      }
      if (positionMic == 3){
        //anguloSul[count] = Serial.read();
        anguloSul[count] = receivedChar;
        count++;
      }
      if (positionMic == 4){
        digitalWrite(13,HIGH); //Indica que chegou no 4o angulo
        //anguloOeste[count] = Serial.read();
        anguloOeste[count] = receivedChar;        
        count++;
      }
    } 
    else {
      positionMic++;
      count = 0;
    }
    if (positionMic == 5){
      positionMic = 1;
      
      delay(2000); // Tempo necessario para o python parar de escrever na USB. Assim, so um programa escreve nela
      digitalWrite(13,LOW); // Indica que ja podemos escrever na porta serial.
      
      Serial.print("Texto: ");
      Serial.println(textoCompleto); // Problema: so esta vindo ";" em textoCompleto
      
      Serial.print ("Angulo Norte: ");
      Serial.println(anguloNorte);
      
      Serial.print ("Angulo Leste: ");
      Serial.println(anguloLeste);
      
      Serial.print ("Angulo Sul: ");
      Serial.println(anguloSul);
            
      Serial.print ("Angulo Oeste: ");
      Serial.println(anguloOeste);
    }
  }
  
  //Fim da Leitura Serial
  //s.write(strtol(anguloNorte));
  //s.write(strtol(anguloLeste));
  //s.write(strtol(anguloSul));
  //s.write(strtol(anguloOeste));
} //Fim do loop
