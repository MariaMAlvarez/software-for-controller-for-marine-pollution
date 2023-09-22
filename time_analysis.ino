#include <X9C.h>

// --------------- PINS X9C --------------------//
#define UD  12
#define INC 13
#define CS  11
X9C pot;
// ---------------------------------------------//

int analog_in_vcg = A11, analog_in_vs = A1, analog_in_va = A2, analog_in_voffset = A3, analog_in_vads = A4;

void setup() {
  Serial.begin(9600);
  pinMode(analog_in_vcg, INPUT);
  pinMode(analog_in_vs, INPUT);
  pinMode(analog_in_va, INPUT);
  pinMode(analog_in_voffset, INPUT);
  pinMode(analog_in_vads, INPUT);
  pot.begin (CS, INC, UD);
  pot.setPot(50, true); // define o potenciometro para metade do wiper
  delay(100);
  Serial.println("Time;Vcg;Vs;Va;Voffset;Vads;/n"); // /n para nao ficar "," e nao causar incoerencias com o script
  delay(500);
  pot.setPot(vcg_value, true); // define o potenciometro para metade do wiper
}

void loop() {
  for (int cycles=0; cycles<num_cycles; cycles++){ //number of cycles 
    pot.setPot(vcg_initial_value, true); // define o potenciometro para a posicao do whiper 
    delay(100);
    for (int steps=0; steps<wiper_steps; steps++){ //number of steps
      float t=millis();
      pot.trimPot(1, X9C_DOWN, true);
      delay (50);

      for (int data_points=0; data_points<num_data_points; data_points++){ //numero de dados por step
        unsigned long t = millis();   
        int vcg = analogRead(analog_in_vcg);
        int vs = analogRead(analog_in_vs);
        int va = analogRead(analog_in_va);
        int voffset = analogRead(analog_in_voffset);
        int vads = analogRead(analog_in_vads);
        unsigned long myArray[6] = {t, vcg, vs, va, voffset, vads};
      
        for (int array=0; array<=5; array++){
        Serial.print(myArray[array]);
        Serial.print(";");
      }
      Serial.println("/n");
      delay(60);
    }
  }
  }
  Serial.println("fim");
  delay(10);
  exit(0);
}
