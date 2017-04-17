#include <string.h>
#include <stdlib.h>
#include <LiquidCrystal.h>
#include <Servo.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7); 

#define MAX_CARACTERS    100
#define MAX_ORDEM_ANGULO 3 + 1
#define PIN_SERVO_NORTE  34    
#define PIN_SERVO_SUL    40

unsigned count;
unsigned positionMic;
char *validacao;
char anguloNorte [MAX_ORDEM_ANGULO];
char anguloLeste [MAX_ORDEM_ANGULO];
char anguloSul [MAX_ORDEM_ANGULO];
char anguloOeste [MAX_ORDEM_ANGULO];
char receivedChar;
//boolean sendAngle;
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
 s_norte.write(0);
 s_sul.write(0); 
}

void loop() { 
  positionMic = 1;
  count = 0;
  //sendAngle = false;

  /*lcd.clear();
  lcd.print(Serial.available());
  delay (333);*/

 while (Serial.available()  == 0) {
  //while (1 > 0) {
    lcd.clear();
    lcd.print("TESTANDO!!");
    delay (2);
  
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
      
      if (positionMic == 4){
        anguloOeste[count] = '\0';
        //sendAngle = true;
      }
      positionMic++;
      count = 0;      
    }
  }
  
  /*if (sendAngle == true){
    Serial.print("Angulo Norte: ");
    Serial.println(anguloNorte);
    Serial.print("Angulo Leste: ");
    Serial.println(anguloLeste);
    Serial.print("Angulo Sul: ");
    Serial.println(anguloSul);
    Serial.print("Angulo Oeste: ");
    Serial.println(anguloOeste);  
    s_norte.write(strtoul(anguloNorte, &validacao, 10));
    //s.write(strtoul(anguloLeste, &validacao, 10));
    s_sul.write(strtoul(anguloSul, &validacao, 10));
    //s.write(strtoul(anguloOeste, &validacao, 10));
  }*/
  s_norte.write(strtoul(anguloNorte, &validacao, 10));
  s_sul.write(strtoul(anguloSul, &validacao, 10));

  /*lcd.clear();
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
