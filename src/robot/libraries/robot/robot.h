#include "arduino_motor_shield.h"
#include "ArduinoMotorShieldR3.h"

namespace BioLab
{
  class Robot
  {
    public:
      // CONSTRUCTORS
      Robot();

      // PUBLIC METHODS
      void initialize();
      void run();

    private:
      BioLab::Motor leftMotor;
      BioLab::Motor rightMotor;
      enum class RobotState { stateStopped, stateRunning };
      RobotState robotState;
      unsigned long startTime;
  };
};
