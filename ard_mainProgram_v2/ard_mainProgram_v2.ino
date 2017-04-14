#include <string.h>
#include <stdlib.h>
#include <LiquidCrystal.h>
#include <Servo.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7); 

#define MAX_CARACTERS    100
#define MAX_ORDEM_ANGULO 3 + 1
#define PIN_SERVO_NORTE  36    
#define PIN_SERVO_SUL    40

unsigned count;
unsigned positionMic;
char *validacao;
Servo s_norte;
Servo s_sul;

char anguloNorte [MAX_ORDEM_ANGULO];
char anguloLeste [MAX_ORDEM_ANGULO];
char anguloSul [MAX_ORDEM_ANGULO];
char anguloOeste [MAX_ORDEM_ANGULO];

void setup()
{
 s_norte.attach(PIN_SERVO_NORTE);
 s_sul.attach(PIN_SERVO_SUL);
 
 Serial.begin(9600);
 pinMode(13,OUTPUT); //para indicar que chegou no 4o angulo (OESTE)
 lcd.begin(16, 2);         // start the library
 lcd.setCursor(0,0);       // set the LCD cursor   position
 s_norte.write(0);
 s_sul.write(0); 
}

char receivedChar;
char textoCompleto[MAX_CARACTERS];
int contador = 0;

void loop() { 
  positionMic = 1;
  count = 0;
  
  while (Serial.available() > 0) {

    receivedChar = Serial.read();
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
        anguloNorte[count] = receivedChar;
        count++;
      }
      if (positionMic == 2){
        anguloLeste[count] = receivedChar;
        count++;
      }
      if (positionMic == 3){
        anguloSul[count] = receivedChar;
        count++;
      }
      if (positionMic == 4){
        digitalWrite(13,HIGH); //Indica que chegou no 4o angulo
        anguloOeste[count] = receivedChar;        
        count++;
      }
    } 
    else {      
      if (positionMic == 1)
        anguloNorte[count] = '\0';
      
      if (positionMic == 2)
        anguloLeste[count] = '\0';
       
      if (positionMic == 3)
        anguloSul[count] = '\0';
      
      if (positionMic == 4)
        anguloOeste[count] = '\0';
      
      positionMic++;
      count = 0;      
    }
  }

  lcd.clear();
  lcd.print("Angulo Norte");
  lcd.setCursor(0,1);
  lcd.print(anguloNorte);
  delay(2000);

  lcd.clear();
  lcd.print("Angulo Leste");
  lcd.setCursor(0,1);
  lcd.print(anguloLeste);
  delay(2000);


  lcd.clear();
  lcd.print("Angulo Sul");
  lcd.setCursor(0,1);
  lcd.print(anguloSul);
  delay(2000);

  lcd.clear();
  lcd.print("Angulo Oeste");
  lcd.setCursor(0,1);
  lcd.print(anguloOeste);
  delay(2000);

  s_norte.write(strtoul(anguloNorte, &validacao, 10));
  //s.write(strtoul(anguloLeste, &validacao, 10));
  s_sul.write(strtoul(anguloSul, &validacao, 10));
  //s.write(strtoul(anguloOeste, &validacao, 10));
} //Fim do loop
