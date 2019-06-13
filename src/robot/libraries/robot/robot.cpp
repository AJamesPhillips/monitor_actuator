#include "robot.h"

// Constructors ////////////////////////////////////////////////////////////////

BioLab::Robot::Robot(): leftMotor(MOTOR::A), rightMotor(MOTOR::B) {}

// Public Methods //////////////////////////////////////////////////////////////

void BioLab::Robot::initialize()
{
  robotState = RobotState::stateStopped;
  startTime = millis();

  // delay(3000);
  // // leftMotor.setSpeed(120);
  // // rightMotor.setSpeed(120);
  // leftMotor.setSpeedAndBrake(-180);
  // rightMotor.setSpeedAndBrake(-180);
  // delay(3000);
  // leftMotor.setSpeedAndBrake(0);
  // rightMotor.setSpeedAndBrake(0);
  // delay(3000);
}

/*
  * @brief Update the state of the robot based on input from sensor and remote control.
  *  Must be called repeatedly while the robot is in operation.
  */
void BioLab::Robot::run()
{
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - startTime;
  if (robotState == RobotState::stateStopped) {
    if (elapsedTime >= 2000) {
      leftMotor.setSpeedAndBrake(120);
      rightMotor.setSpeedAndBrake(120);
      robotState = RobotState::stateRunning;
      startTime = currentTime;
    }
  }
  else if (robotState == RobotState::stateRunning) {
    if (elapsedTime >= 1000) {
      leftMotor.setSpeedAndBrake(0);
      rightMotor.setSpeedAndBrake(0);
      robotState = RobotState::stateStopped;
      startTime = currentTime;
    }
  }
}
