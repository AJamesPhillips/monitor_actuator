#include "ArduinoMotorShieldR3.h"

ArduinoMotorShieldR3 md;

void setup()
{
  Serial.begin(9600);
  Serial.println("Arduino Motor Shield R3");
  md.init();
}

void loop()
{
  Serial.println("M1 Speed 100% Forward");
  md.setM1Speed(255);
  Serial.println("M2 Speed 100% Forward");
  md.setM2Speed(255);
  delay(3000);

  md.setBrakes();
  delay(1000);

  md.setM1Speed(-255);
  md.setM2Speed(-255);
  delay(3000);

  md.setBrakes();
  delay(1000);
}
