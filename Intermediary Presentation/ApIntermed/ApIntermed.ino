#include <string.h>
#include <stdlib.h>
#include <LiquidCrystal.h>
#include <Servo.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7); 

#define MAX_ORDEM_ANGULO 3 + 1               

#define PIN_SERVO_NORTE  44
#define PIN_SERVO_LESTE  38
#define PIN_SERVO_SUL    32
#define PIN_SERVO_OESTE  26

unsigned count;
unsigned positionMic;
unsigned contadorTexto;
unsigned contadorAngulo;
unsigned contadorStringAng;
char *validacao;
char stringAngNorte [MAX_ORDEM_ANGULO];
char stringAngLeste [MAX_ORDEM_ANGULO];
char stringAngSul [MAX_ORDEM_ANGULO];
char stringAngOeste [MAX_ORDEM_ANGULO];
char textoCompleto[20];
char receivedChar;

Servo s_norte;
Servo s_leste;
Servo s_sul;
Servo s_oeste;

boolean firstLoop = false;
unsigned anguloNorte = 90;
unsigned anguloLeste = 90; 
unsigned anguloSul = 90;
unsigned anguloOeste = 90;

void setup()
{
   s_norte.attach(PIN_SERVO_NORTE);
   s_leste.attach(PIN_SERVO_LESTE);
   s_sul.attach(PIN_SERVO_SUL);
   s_oeste.attach(PIN_SERVO_OESTE);
   
   Serial.begin(9600);
   pinMode(13,OUTPUT); //para indicar que chegou no 4o angulo (OESTE)

   lcd.begin(16, 2);         // start the library
   lcd.setCursor(0,0);       // set the LCD cursor   position
   lcd.print("HELLO!");
   
   s_norte.write(45);
   s_leste.write(45);
   s_sul.write(45); 
   s_oeste.write(45);
   delay(1000);
   s_norte.write(90);
   s_leste.write(90);
   s_sul.write(90); 
   s_oeste.write(90);
}

void loop() { 
    contadorAngulo = 0;
    contadorStringAng = 0;
    positionMic = 1;
    count = 0;
    contadorTexto = 0;
  
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
    }
    
    
    Serial.println(".");
  //  Serial.flush();
    
    if (firstLoop){
      firstLoop = false;
      textoCompleto[contadorTexto]='\0';
      for (contadorTexto = 0; contadorAngulo < 4; contadorTexto++){
        if (textoCompleto[contadorTexto] != ';'){
          if (contadorAngulo == 0)
            stringAngNorte[contadorStringAng] = textoCompleto[contadorTexto];
          
          if (contadorAngulo == 1)
            stringAngLeste[contadorStringAng] = textoCompleto[contadorTexto];
            
          if (contadorAngulo == 2)
            stringAngSul[contadorStringAng] = textoCompleto[contadorTexto];
            
          if (contadorAngulo == 3)
            stringAngOeste[contadorStringAng] = textoCompleto[contadorTexto];
          
          contadorStringAng++;        
        }
  
        else{
          if (contadorAngulo == 0)
            stringAngNorte[contadorStringAng] = '\0';
            
          if (contadorAngulo == 1)
            stringAngLeste[contadorStringAng] = '\0';
              
          if (contadorAngulo == 2)
            stringAngSul[contadorStringAng] = '\0';
              
          if (contadorAngulo == 3)
            stringAngOeste[contadorStringAng] = '\0';
          
          contadorStringAng = 0;
          contadorAngulo++;
        }
      } //End for
      
      anguloNorte = strtoul(stringAngNorte, &validacao, 10);
      if ((anguloNorte >= 0) && (anguloNorte <= 180))
        s_norte.write(anguloNorte);
      
      anguloLeste = strtoul(stringAngLeste, &validacao, 10);
      if ((anguloLeste >= 0) && (anguloLeste <= 180))
        s_leste.write(anguloLeste);
    
      anguloSul = strtoul(stringAngSul, &validacao, 10);
      if ((anguloSul >= 0) && (anguloSul <= 180))
        s_sul.write(anguloSul);
      
      anguloOeste = strtoul(stringAngOeste, &validacao, 10);
      if ((anguloOeste >= 0) && (anguloOeste <= 180))  
        s_oeste.write(anguloOeste);
        
    } //End if(firstLoop)
    
    lcd.clear();
    lcd.print("Texto Completo");
    lcd.setCursor(1,1);
    lcd.print(textoCompleto);
    delay(1000);
    
    /*
    lcd.clear();
    lcd.print("Angulo Norte");
    lcd.setCursor(1,1);
    lcd.print(anguloNorte);  
    delay(500);
  
    lcd.clear();
    lcd.print("Angulo Leste");
    lcd.setCursor(1,1);
    lcd.print(anguloLeste);  
    delay(500);
  
    lcd.clear();
    lcd.print("Angulo Sul");
    lcd.setCursor(1,1);
    lcd.print(anguloSul);
    delay(500);
  
    lcd.clear();
    lcd.print("Angulo Oeste");
    lcd.setCursor(1,1);
    lcd.print(anguloOeste);  
    delay(500);
    */
} //Fim do loop

