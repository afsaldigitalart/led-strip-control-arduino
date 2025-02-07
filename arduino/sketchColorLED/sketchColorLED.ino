#include <EEPROM.h>
const int redP = 5;
const int greenP = 11;
const int blueP = 9;
void setup() {
  Serial.begin(9600);
  pinMode(redP, OUTPUT);
  pinMode(greenP, OUTPUT);
  pinMode(blueP, OUTPUT);
}

void loop() {
  if (Serial.available()>=3){
    byte red = Serial.read();
    byte green = Serial.read();
    byte blue = Serial.read();

    EEPROM.write(0, red);
    EEPROM.write(1, green);
    EEPROM.write(2, blue);

    analogWrite(redP, red);
    analogWrite(greenP, green);
    analogWrite(blueP, blue);
  }

}
