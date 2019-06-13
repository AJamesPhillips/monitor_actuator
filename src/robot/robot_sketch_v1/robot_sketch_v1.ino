#include "arduino_motor_shield.h"
#include "ArduinoMotorShieldR3.h"

BioLab::Motor motor1(MOTOR::A);
BioLab::Motor motor2(MOTOR::B);

void setup()
{
  Serial.begin(9600);
  Serial.println("Arduino Motor Shield R3");
  BioLab::Motor motor1(MOTOR::A);
  BioLab::Motor motor2(MOTOR::B);
}

void loop()
{
  motor1.setSpeedAndBrake(-180);
  motor2.setSpeedAndBrake(-180);
  delay(1000);
  motor1.setSpeedAndBrake(0);
  motor2.setSpeedAndBrake(0);
  delay(3000);

  // // md.setBrakes(false);
  // Serial.println("M1 Speed 100% Forward");
  // md.setSpeed(255, MOTOR::A);
  // Serial.println("M2 Speed 100% Forward");
  // md.setM2Speed(255);
  // delay(100);

  // md.setBrakes(true);
  // delay(1000);

  // md.setBrakes(false);
  // md.setM1Speed(-255);
  // md.setM2Speed(-255);
  // delay(3000);

  // md.setBrakes(true);
  // delay(1000);
}
