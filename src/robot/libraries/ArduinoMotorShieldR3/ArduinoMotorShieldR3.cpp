#include "ArduinoMotorShieldR3.h"
#include "logging.h"

// Constructors ////////////////////////////////////////////////////////////////
ArduinoMotorShieldR3::ArduinoMotorShieldR3()
{
  //Pin map
  DIR_A = 12;
  BRK_A = 9;
  PWM_A = 3;
  CS_A = A0; // 14

  DIR_B = 13;
  BRK_B = 8;
  PWM_B = 11;
  CS_B = A1; // 15
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
void ArduinoMotorShieldR3::setSpeed(int speed, MOTOR motor)
{
  bool dir = HIGH;
  if (speed < 0) {
    speed = -speed;  // Make speed a positive quantity
    dir = LOW;
  }
  digitalWrite(dirPin(motor), dir);

  if (speed > 255) {
    // Max PWM dutycycle
    speed = 255;
  }
  logIt("setSpeed direction: %d (pin %d) speed: %d (pin %d)", dir, dirPin(motor), speed, pwmPin(motor));
  analogWrite(pwmPin(motor), speed);
}

// // Set speed for motor 1, speed is a number between -255 and 255
// // Motor 1 == Motor A
// void ArduinoMotorShieldR3::setM1Speed(int speed)
// {
//   setSpeed(speed, MOTOR::A);
// }

// // Set speed for motor 2, speed is a number between -255 and 255
// // Motor B == Motor B
// void ArduinoMotorShieldR3::setM2Speed(int speed)
// {
//   setSpeed(speed, MOTOR::B);
// }

// // Set speed for motor 1 and 2
// void ArduinoMotorShieldR3::setSpeeds(int m1Speed, int m2Speed)
// {
//   setM1Speed(m1Speed);
//   setM2Speed(m2Speed);
// }

// Brake motor 1
void ArduinoMotorShieldR3::setBrake(bool state, MOTOR motor)
{
  logIt("setBrake %d (pin %d)", state, brkPin(motor));
  digitalWrite(brkPin(motor), state);
}

// // Brake motor 1
// void ArduinoMotorShieldR3::setM1Brake(bool state)
// {
//   digitalWrite(brkPin(MOTOR::A), state);
// }

// // Brake motor 2
// void ArduinoMotorShieldR3::setM2Brake(bool state)
// {
//   digitalWrite(brkPin(MOTOR::B), state);
// }

// // Brake motor 1 and 2
// void ArduinoMotorShieldR3::setBrakes(bool state)
// {
//   setM1Brake(state);
//   setM2Brake(state);
// }

// TODO: check this calculation
// Return motor 1 current value in milliamps.
unsigned int ArduinoMotorShieldR3::getM1CurrentMilliamps()
{
  // 5 V / 1024 ADC counts = 4.88 mV per count
  // 3.3 V = 2.0 A; 3.3 V / 4.88 mv per count = 676 counts
  // 2.0 A / 676 counts = 2.96 mA per count
  return analogRead(csPin(MOTOR::A)) * 2.96;
}

// TODO: check this calculation
// Return motor 2 current value in milliamps.
unsigned int ArduinoMotorShieldR3::getM2CurrentMilliamps()
{
  // 5 V / 1024 ADC counts = 4.88 mV per count
  // 3.3 V = 2.0 A; 3.3 V / 4.88 mv per count = 676 counts
  // 2.0 A / 676 counts = 2.96 mA per count
  return analogRead(csPin(MOTOR::B)) * 2.96;
}

// Private Methods /////////////////////////////////////////////////////////////

unsigned char ArduinoMotorShieldR3::dirPin(MOTOR motor)
{
  return motor == MOTOR::A ? DIR_A : DIR_B;
}

unsigned char ArduinoMotorShieldR3::brkPin(MOTOR motor)
{
  return motor == MOTOR::A ? BRK_A : BRK_B;
}

unsigned char ArduinoMotorShieldR3::pwmPin(MOTOR motor)
{
  return motor == MOTOR::A ? PWM_A : PWM_B;
}

unsigned char ArduinoMotorShieldR3::csPin(MOTOR motor)
{
  return motor == MOTOR::A ? CS_A : CS_B;
}
