#include <X9C.h>

// --------------- PINS X9C --------------------//
#define UD  12
#define INC 13
#define CS  11
X9C pot;
// ---------------------------------------------//

int analog_in_vcg = A0, analog_in_vs = A1, analog_in_va = A2, analog_in_voffset = A3, analog_in_vadc = A4;

void setup() {
  Serial.begin(9600);
  pinMode(analog_in_vcg, INPUT);
  pinMode(analog_in_vs, INPUT);
  pinMode(analog_in_va, INPUT);
  pinMode(analog_in_voffset, INPUT);
  pinMode(analog_in_vadc, INPUT);
  pot.begin (CS, INC, UD);
  pot.setPot(50, true); // define o potenciometro para metade do wiper
  delay(100);
  Serial.println("Time;Vcg;Vs;Va;Voffset;Vadc;/n"); // /n para nao ficar "," e nao causar incoerencias com o script
  delay(1000);
}

void loop() {
  for (int cycles=0; cycles<2; cycles++){ //number of cycles 
    pot.setPot(59, true); // define o potenciometro para a posicao do whiper 
    delay(500);
    for (int steps=0; steps<39; steps++){ //number of steps
      float t=millis();
      pot.trimPot(1, X9C_DOWN, true);
      delay (500);

      for (int data_points=0; data_points<10; data_points++){ //numero de dados por step
        unsigned long t = millis();   
        int vcg = analogRead(analog_in_vcg);
        int vs = analogRead(analog_in_vs);
        int va = analogRead(analog_in_va);
        int voffset = analogRead(analog_in_voffset);
        int vadc = analogRead(analog_in_vadc);
        unsigned long myArray[6] = {t, vcg, vs, va, voffset, vadc};
      
        for (int array=0; array<=5; array++){
        Serial.print(myArray[array]);
        Serial.print(";");
      }
      Serial.println("/n");
      delay(600);
    }
  }
  }
  Serial.println("fim");
  delay(10);
  exit(0);
}
