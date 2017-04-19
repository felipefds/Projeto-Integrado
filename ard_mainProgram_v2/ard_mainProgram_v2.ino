#include <string.h>
#include <stdlib.h>
#include <LiquidCrystal.h>
#include <Servo.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7); 

#define MAX_ORDEM_ANGULO 3 + 1               
#define PIN_SERVO_NORTE  26
#define PIN_SERVO_SUL    40

unsigned count;
unsigned positionMic;
unsigned contadorTexto;
char *validacao;
char anguloNorte [MAX_ORDEM_ANGULO];
char anguloLeste [MAX_ORDEM_ANGULO];
char anguloSul [MAX_ORDEM_ANGULO];
char anguloOeste [MAX_ORDEM_ANGULO];
char textoCompleto[20];
char receivedChar;

Servo s_norte;
Servo s_sul;

void setup()
{
 s_norte.attach(PIN_SERVO_NORTE);
 s_sul.attach(PIN_SERVO_SUL);
 
 Serial.begin(9600);
 pinMode(13,OUTPUT); //para indicar que chegou no 4o angulo (OESTE)
 lcd.begin(16, 2);         // start the library
 lcd.setCursor(0,0);       // set the LCD cursor   position
 s_norte.write(90);
 s_sul.write(90); 
}

void loop() { 
  positionMic = 1;
  count = 0;

 while (Serial.available() > 0) {

//    lcd.clear();
//    lcd.print("Status Serial");
//    lcd.setCursor(0,1);
//    lcd.print(Serial.available());
//    delay(1000);
//     
    receivedChar = Serial.read();
    textoCompleto[contadorTexto]=receivedChar;
    contadorTexto++;

/*    lcd.clear();
    lcd.print("CHAR RECEBIDO");
    lcd.setCursor(0,1);
    lcd.print(receivedChar);  
    delay(1000);*/
    
    if (receivedChar != ';'){
      if (positionMic == 1){
//        lcd.clear();
//        lcd.print("CHAR ANGULO NORTE");
//        lcd.setCursor(0,1);
//        lcd.print(receivedChar);  
//        delay(1000);
        anguloNorte[count] = receivedChar;
      }
      if (positionMic == 2){
//        lcd.clear();
//        lcd.print("CHAR ANGULO LESTE");
//        lcd.setCursor(0,1);
//        lcd.print(receivedChar);  
//        delay(1000);
        anguloLeste[count] = receivedChar;
      }
      if (positionMic == 3){
//        lcd.clear();
//        lcd.print("CHAR ANGULO SUL");
//        lcd.setCursor(0,1);
//        lcd.print(receivedChar);  
//        delay(1000);
        anguloSul[count] = receivedChar;
      }
      if (positionMic == 4){
//        lcd.clear();
//        lcd.print("CHAR ANGULO OESTE");
//        lcd.setCursor(0,1);
//        lcd.print(receivedChar);  
//        delay(1000);
        digitalWrite(13,HIGH); //Indica que chegou no 4o angulo
        anguloOeste[count] = receivedChar;
      }
      count++;
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

      positionMic=positionMic+1;
      count = 0;
    }
  }
  textoCompleto[contadorTexto]='\0';
  Serial.println(".");
  lcd.clear();
  lcd.print("Texto Complete");
  lcd.setCursor(0,1);
  lcd.print(textoCompleto);
  
  s_norte.write(strtoul(anguloNorte, &validacao, 10));
  //s.write(strtoul(anguloLeste, &validacao, 10));
  s_sul.write(strtoul(anguloSul, &validacao, 10));
  //s.write(strtoul(anguloOeste, &validacao, 10));

/*  lcd.clear();
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
  delay(2000);*/
} //Fim do loop
