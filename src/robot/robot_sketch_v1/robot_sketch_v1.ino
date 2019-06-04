#include "ArduinoMotorShieldR3.h"

ArduinoMotorShieldR3 md;

void setup()
{
  Serial.begin(115200);
  Serial.println("Arduino Motor Shield R3");
  md.init();
}

void loop()
{
  Serial.println("M1 Speed 100% Forward");
  md.setM1Speed(400);
  Serial.println("M2 Speed 100% Forward");
  md.setM2Speed(400);

void setup() {
  //    Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT); //Initiates Motor Channel A pin
  pinMode(9, OUTPUT); //Initiates Brake Channel A pin
}

void loop() {

  //  Serial.println("Hello, world!");
  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);

  //forward
  digitalWrite(12, HIGH); //Establishes forward direction of Channel A
  digitalWrite(9, LOW);   //Disengage the Brake for Channel A
  analogWrite(3, 255);   //Spins the motor on Channel A (max speed is 255)

  delay(3000);

  digitalWrite(9, HIGH); //Engage the Brake for Channel A

  delay(1000);

  //backward
  digitalWrite(12, LOW); //Establishes backward direction of Channel A
  digitalWrite(9, LOW);   //Disengage the Brake for Channel A
  analogWrite(3, 123);   //Spins the motor on Channel A slower

  delay(3000);

  digitalWrite(9, HIGH); //Engage the Brake for Channel A

  delay(1000);
}
