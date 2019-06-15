#include "arduino_motor_shield.h"

// Constructors ////////////////////////////////////////////////////////////////

BioLab::Motor::Motor(MOTOR _motorID): MotorDriver(), motorID(_motorID), motor(), currentRequestedSpeed(0)
{
  motor.init(); // smells, TODO: refactor
}

// Public Methods //////////////////////////////////////////////////////////////

void BioLab::Motor::setSpeed(int speed)
{
    if (currentRequestedSpeed != speed) {
        currentRequestedSpeed = speed;
        motor.setSpeed(speed, motorID);
    }
}

void BioLab::Motor::setBrake(bool state) {
    if (state && currentRequestedSpeed != 0) {
        setSpeed(0);
    }
    motor.setBrake(state, motorID);
}

void BioLab::Motor::setSpeedAndBrake(int speed)
{
    setBrake(speed == 0);
    setSpeed(speed);
}

int BioLab::Motor::getRequestedSpeed() const
{
    return currentRequestedSpeed;
}
