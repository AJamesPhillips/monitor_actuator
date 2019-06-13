#include "arduino_motor_shield.h"
#include "ArduinoMotorShieldR3.h"

namespace BioLab
{
  class Robot
  {
    public:
      /*
        * @brief Class constructor.
        */
      Robot(): leftMotor(MOTOR::A), rightMotor(MOTOR::B)
      {
        // initialize();
      }

      /*
        * @brief Initialize the robot state.
        */
      void initialize()
      {
        delay(3000);
        // leftMotor.setSpeed(120);
        // rightMotor.setSpeed(120);
        leftMotor.setSpeedAndBrake(-180);
        rightMotor.setSpeedAndBrake(-180);
        delay(3000);
        leftMotor.setSpeedAndBrake(0);
        rightMotor.setSpeedAndBrake(0);
        delay(3000);
      }

      /*
        * @brief Update the state of the robot based on input from sensor and remote control.
        *  Must be called repeatedly while the robot is in operation.
        */
      void run()
      {
      }

    private:
      BioLab::Motor leftMotor;
      BioLab::Motor rightMotor;
  };
};
