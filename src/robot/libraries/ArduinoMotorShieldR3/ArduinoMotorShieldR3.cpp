#include "ArduinoMotorShieldR3.h"

// Constructors ////////////////////////////////////////////////////////////////

ArduinoMotorShieldR3::ArduinoMotorShieldR3()
{
  //Pin map
  DIR_A = 12;
  BRK_A = 9;
  PWM_A = 3;
  CS_A = A0;

  DIR_B = 13;
  BRK_B = 8;
  PWM_B = 11;
  CS_B = A1;
}

ArduinoMotorShieldR3::ArduinoMotorShieldR3(
    unsigned char DIR_A, unsigned char BRK_A, unsigned char PWM_A, unsigned char CS_A,
    unsigned char DIR_B, unsigned char BRK_B, unsigned char PWM_B, unsigned char CS_B)
{
  //Pin map
  this->DIR_A = DIR_A;
  this->BRK_A = BRK_A;
  this->PWM_A = PWM_A;
  this->CS_A = CS_A;

  this->DIR_B = DIR_B;
  this->BRK_B = BRK_B;
  this->PWM_B = PWM_B;
  this->CS_B = CS_B;
}

// Public Methods //////////////////////////////////////////////////////////////
void ArduinoMotorShieldR3::init()
{
  // Define pinMode for the pins and set the frequency for timer1.
  pinMode(DIR_A,OUTPUT);
  pinMode(BRK_A,OUTPUT);
  pinMode(PWM_A,OUTPUT);
  pinMode(CS_A,INPUT);

  pinMode(DIR_B,OUTPUT);
  pinMode(BRK_B,OUTPUT);
  pinMode(PWM_B,OUTPUT);
  pinMode(CS_B,INPUT);
}

// Set speed for a motor, speed is a number between -255 and 255
// Private
void ArduinoMotorShieldR3::setSpeed(int speed, unsigned char DIR, unsigned char PWM)
{
  if (speed < 0) {
    speed = -speed;  // Make speed a positive quantity
    digitalWrite(DIR, LOW);
  }
  else {
    digitalWrite(DIR, HIGH);
  }

  if (speed > 255) {
    // Max PWM dutycycle
    speed = 255;
  }

  analogWrite(PWM, speed); // default to using analogWrite
}

// Set speed for motor 1, speed is a number between -255 and 255
// Motor 1 == Motor A
void ArduinoMotorShieldR3::setM1Speed(int speed)
{
  setSpeed(speed, DIR_A, PWM_A);
}

// Set speed for motor 2, speed is a number between -255 and 255
// Motor B == Motor B
void ArduinoMotorShieldR3::setM2Speed(int speed)
{
  setSpeed(speed, DIR_B, PWM_B);
}

// Set speed for motor 1 and 2
void ArduinoMotorShieldR3::setSpeeds(int m1Speed, int m2Speed)
{
  setM1Speed(m1Speed);
  setM2Speed(m2Speed);
}

// Brake motor 1
void ArduinoMotorShieldR3::setM1Brake()
{
  digitalWrite(BRK_A, HIGH);
}

// Brake motor 2
void ArduinoMotorShieldR3::setM2Brake()
{
  digitalWrite(BRK_B, HIGH);
}

// Brake motor 1 and 2
void ArduinoMotorShieldR3::setBrakes()
{
  setM1Brake();
  setM2Brake();
}

// TODO: check this calculation
// Return motor 1 current value in milliamps.
unsigned int ArduinoMotorShieldR3::getM1CurrentMilliamps()
{
  // 5 V / 1024 ADC counts = 4.88 mV per count
  // 3.3 V = 2.0 A; 3.3 V / 4.88 mv per count = 676 counts
  // 2.0 A / 676 counts = 2.96 mA per count
  return analogRead(CS_A) * 2.96;
}

// TODO: check this calculation
// Return motor 2 current value in milliamps.
unsigned int ArduinoMotorShieldR3::getM2CurrentMilliamps()
{
  // 5 V / 1024 ADC counts = 4.88 mV per count
  // 3.3 V = 2.0 A; 3.3 V / 4.88 mv per count = 676 counts
  // 2.0 A / 676 counts = 2.96 mA per count
  return analogRead(CS_B) * 2.96;
}

