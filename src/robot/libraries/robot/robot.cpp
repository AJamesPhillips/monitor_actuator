#include "robot.h"
#include "logging.h"

// Constructors ////////////////////////////////////////////////////////////////

BioLab::Robot::Robot(): leftMotor(MOTOR::A), rightMotor(MOTOR::B) {}

// Public Methods //////////////////////////////////////////////////////////////

void BioLab::Robot::initialize()
{
  logIt("BioLab::Robot::initialize");
  robotState = RobotState::stateStopped;
  currentActionStateTime = -1;
}

/*
  * @brief Update the state of the robot based on input from sensor and remote control.
  *  Must be called repeatedly while the robot is in operation.
  */
void BioLab::Robot::run()
{
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - currentActionStateTime;
  if (robotState == RobotState::stateStopped) {
    if (elapsedTime >= 1000 || currentActionStateTime < 0) {
      logIt("Starting...");
      // leftMotor.setSpeedAndBrake(255);
      // rightMotor.setSpeedAndBrake(255);
      robotState = RobotState::stateRunning;
      currentActionStateTime = currentTime;
    }
  }
  else if (robotState == RobotState::stateRunning) {
    if (elapsedTime >= 20000) {
      logIt("Stop.");
      // leftMotor.setSpeedAndBrake(0);
      // rightMotor.setSpeedAndBrake(0);
      robotState = RobotState::stateStopped;
      currentActionStateTime = currentTime;
    }
  }
}
