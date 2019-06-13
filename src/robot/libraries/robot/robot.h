#include "arduino_motor_shield.h"
#include "ArduinoMotorShieldR3.h"

#ifdef LOGGING

// logging is enabled
#include <stdarg.h>

void log(char* format, ...)
{
    char line[1024];
    va_list args;
    va_start(args, format);
    vsnprintf(line, sizeof(line), format, args);
    va_end(args);
    Serial.print(line);
}

#else

// logging is disabled
#define log(...)

#endif

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
