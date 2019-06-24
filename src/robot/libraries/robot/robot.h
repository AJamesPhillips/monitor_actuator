#include "arduino_motor_shield.h"
#include "ArduinoMotorShieldR3.h"

namespace BioLab
{
  enum class RobotMotor {
    Left,
    Right
  };

  class Robot
  {
    public:
      // CONSTRUCTORS
      Robot();

      // PUBLIC METHODS
      void initialize();
      void update();
      void move(RobotMotor motor, int power, unsigned long durationMs);

    private:
      BioLab::Motor leftMotor;
      BioLab::Motor rightMotor;
      // enum class RobotState { stateStopped, stateRunning };
      // RobotState robotState;
      unsigned long leftMotorActionStateTime;
      unsigned long leftMotorDurationMs;
      unsigned long rightMotorActionStateTime;
      unsigned long rightMotorDurationMs;
  };
};
