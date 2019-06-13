#ifndef ArduinoMotorShieldR3_h
#define ArduinoMotorShieldR3_h

#include <Arduino.h>

enum class MOTOR { A, B };

class ArduinoMotorShieldR3
{
  public:
    // CONSTRUCTORS
    ArduinoMotorShieldR3(); // Default pin selection.
    ArduinoMotorShieldR3( // User-defined pin selection.
        unsigned char DIR_A, unsigned char BRK_A, unsigned char PWM_A, unsigned char CS_A,
        unsigned char DIR_B, unsigned char BRK_B, unsigned char PWM_B, unsigned char CS_B);

    // PUBLIC METHODS
    void init(); // Initialize TIMER 1, set the PWM to 20kHZ.
    // void setM1Speed(int speed); // Set speed for M1.
    // void setM2Speed(int speed); // Set speed for M2.
    // void setSpeeds(int m1Speed, int m2Speed); // Set speed for both M1 and M2.
    void setSpeed(int speed, MOTOR motor); // Set speed
    // void setM1Brake(bool state); // Brake M1.
    // void setM2Brake(bool state); // Brake M2.
    // void setBrakes(bool state); // Brake both M1 and M2.
    void setBrake(bool state, MOTOR motor);
    unsigned int getM1CurrentMilliamps(); // Get current reading for M1.
    unsigned int getM2CurrentMilliamps(); // Get current reading for M2.

  private:
    unsigned char DIR_A;
    unsigned char BRK_A;
    unsigned char PWM_A;
    unsigned char CS_A;

    unsigned char DIR_B;
    unsigned char BRK_B;
    unsigned char PWM_B;
    unsigned char CS_B;

    unsigned char dirPin(MOTOR motor);
    unsigned char brkPin(MOTOR motor);
    unsigned char pwmPin(MOTOR motor);
    unsigned char csPin(MOTOR motor);
};

#endif
