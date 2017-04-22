#include <string.h>
#include <stdlib.h>
#include <LiquidCrystal.h>
#include <Servo.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12); 

#define MAX_ORDEM_ANGULO 3 + 1               
#define PIN_SERVO_NORTE  13
#define PIN_SERVO_LESTE  2
#define PIN_SERVO_SUL    3
#define PIN_SERVO_OESTE  4

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
Servo s_leste;
Servo s_sul;
Servo s_oeste;

boolean firstLoop = false;
unsigned angulo;

void setup()
{
 s_norte.attach(PIN_SERVO_NORTE);
 s_leste.attach(PIN_SERVO_LESTE);
 s_sul.attach(PIN_SERVO_SUL);
 s_oeste.attach(PIN_SERVO_OESTE);
 
 Serial.begin(9600);
 pinMode(13,OUTPUT); //para indicar que chegou no 4o angulo (OESTE)
 pinMode(5,OUTPUT);
 analogWrite(5,96);
 lcd.begin(16, 2);         // start the library
 lcd.setCursor(0,0);       // set the LCD cursor   position
 lcd.print("HELLO!");
 s_norte.write(90);
 s_leste.write(90);
 s_sul.write(90); 
 s_oeste.write(90);
}

void loop() { 
  positionMic = 1;
  count = 0;

 while (Serial.available() > 0) {

    firstLoop = true;
//    lcd.clear();
//    lcd.print("Status Serial");
//    lcd.setCursor(1,0);
//    lcd.print(Serial.available());
//    delay(1000);
//     
    receivedChar = Serial.read();
    textoCompleto[contadorTexto]=receivedChar;
    contadorTexto++;

//    lcd.clear();
//    lcd.print("CHAR RECEBIDO");
//    lcd.setCursor(1,1);
//    lcd.print(receivedChar);  
//    delay(500);
    
    if (receivedChar != ';'){      
      if (positionMic == 1){
//        lcd.clear();
//        lcd.print("CHAR ANG NORTE");
//        lcd.setCursor(1,1);
//        lcd.print(receivedChar);  
//        delay(1000);
        anguloNorte[count] = receivedChar;
      }
      if (positionMic == 2){
//        lcd.clear();
//        lcd.print("CHAR ANG LESTE");
//        lcd.setCursor(1,1);
//        lcd.print(receivedChar);  
//        delay(1000);
        anguloLeste[count] = receivedChar;
      }
      if (positionMic == 3){
//        lcd.clear();
//        lcd.print("CHAR ANG SUL");
//        lcd.setCursor(1,1);
//        lcd.print(receivedChar);  
//        delay(1000);
        anguloSul[count] = receivedChar;
      }
      if (positionMic == 4){
//        lcd.clear();
//        lcd.print("CHAR ANG OESTE");
//        lcd.setCursor(1,1);
//        lcd.print(receivedChar);  
//        delay(1000);
        //digitalWrite(13,HIGH); //Indica que chegou no 4o angulo
        anguloOeste[count] = receivedChar;
      }
      count++;
    } 
    else {
         lcd.clear();
        lcd.print("anguloSul ats");
        lcd.setCursor(1,1);
        lcd.print(anguloSul);
        delay(1000);
        lcd.clear();
      if (positionMic == 1)
        anguloNorte[count] = '\0';
      
      if (positionMic == 2)
        anguloLeste[count] = '\0';
       
      if (positionMic == 3){
        delay(500);
        anguloSul[count] = '\0';
        lcd.clear();
        lcd.print("anguloSul dps");
        lcd.setCursor(1,1);
        lcd.print(anguloSul);
        delay(1000);
        lcd.clear();
        delay(500);
      }
      if (positionMic == 4){
        anguloOeste[count] = '\0';
//        lcd.clear();
//        lcd.print("anguloSul EOS");
//        lcd.setCursor(1,1);
//        lcd.print(anguloSul);
//        delay(1000);
      }
      positionMic=positionMic+1;
      count = 0;
    }
  }
//  textoCompleto[contadorTexto]='\0';
//  Serial.println(".");
//  lcd.clear();
//  lcd.print("Texto Complete");
//  lcd.setCursor(1,1);
//  lcd.print(textoCompleto);

  
  if (firstLoop){
    firstLoop=false;
    angulo = strtoul(anguloNorte, &validacao, 10);
    if ((angulo >= 0) && (angulo <= 180))
      s_norte.write(angulo);
    
    angulo = strtoul(anguloLeste, &validacao, 10);
    if ((angulo >= 0) && (angulo <= 180))
      s_leste.write(angulo);
  
    angulo = strtoul(anguloSul, &validacao, 10);
//    lcd.clear();
//    lcd.print(anguloSul);
//    lcd.setCursor(1,1);
//    lcd.print(angulo);
//    delay(1000);
    if ((angulo >= 0) && (angulo <= 180))
      s_sul.write(angulo);
    
    angulo = strtoul(anguloOeste, &validacao, 10);
    if ((angulo >= 0) && (angulo <= 180))  
      s_oeste.write(angulo);
  }
//  lcd.clear();
//  lcd.print("Angulo Norte");
//  lcd.setCursor(1,1);
//  lcd.print(anguloNorte);  
//  delay(2000);
//
//  lcd.clear();
//  lcd.print("Angulo Leste");
//  lcd.setCursor(1,1);
//  lcd.print(anguloLeste);  
//  delay(2000);
//
//  lcd.clear();
//  lcd.print("Angulo Sul");
//  lcd.setCursor(1,1);
//  lcd.print(anguloSul);
//  delay(2000);
//
//  lcd.clear();
//  lcd.print("Angulo Oeste");
//  lcd.setCursor(1,1);
//  lcd.print(anguloOeste);  
//  delay(2000);
} //Fim do loop
