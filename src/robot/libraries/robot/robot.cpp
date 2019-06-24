#include "robot.h"
#include "logging.h"

// Constructors ////////////////////////////////////////////////////////////////

BioLab::Robot::Robot(): leftMotor(MOTOR::A), rightMotor(MOTOR::B) {}

// Public Methods //////////////////////////////////////////////////////////////

void BioLab::Robot::initialize()
{
  logIt("BioLab::Robot::initialize");
  // robotState = RobotState::stateStopped;
  leftMotorActionStateTime = 0;
  leftMotorDurationMs = 0;
  rightMotorActionStateTime = 0;
  rightMotorDurationMs = 0;
}

/*
  * @brief Update the state of the robot based on previous requests.
  *  Must be called repeatedly while the robot is in operation.
  */
void BioLab::Robot::update()
{
  unsigned long currentTime = millis();
  if (leftMotorDurationMs != 0 && (leftMotorActionStateTime + leftMotorDurationMs) < currentTime)
  {
    leftMotor.setSpeedAndBrake(0);
    leftMotorDurationMs = 0;
  }

  if (rightMotorDurationMs != 0 && (rightMotorActionStateTime + rightMotorDurationMs) < currentTime)
  {
    rightMotor.setSpeedAndBrake(0);
    rightMotorDurationMs = 0;
  }
}

/*
  * @brief Update the desired state of the robot based on input from remote control.
  */
void BioLab::Robot::move(BioLab::RobotMotor motor, int power, unsigned long durationMs)
{
  unsigned long currentTime = millis();

  if (motor == BioLab::RobotMotor::Left)
  {
    leftMotor.setSpeedAndBrake(power);
    leftMotorActionStateTime = currentTime;
    leftMotorDurationMs = durationMs;
  }
  else if (motor == BioLab::RobotMotor::Right)
  {
    rightMotor.setSpeedAndBrake(power);
    rightMotorActionStateTime = currentTime;
    rightMotorDurationMs = durationMs;
  }

  //
  // unsigned long elapsedTime = currentTime - currentActionStateTime;
  // if (robotState == RobotState::stateStopped) {
  //   if (elapsedTime >= 1000 || currentActionStateTime < 0) {
  //     logIt("Starting...");
  //     // leftMotor.setSpeedAndBrake(255);
  //     // rightMotor.setSpeedAndBrake(255);
  //     robotState = RobotState::stateRunning;
  //     currentActionStateTime = currentTime;
  //   }
  // }
  // else if (robotState == RobotState::stateRunning) {
  //   if (elapsedTime >= 20000) {
  //     logIt("Stop.");
  //     // leftMotor.setSpeedAndBrake(0);
  //     // rightMotor.setSpeedAndBrake(0);
  //     robotState = RobotState::stateStopped;
  //     currentActionStateTime = currentTime;
  //   }
  // }
}
