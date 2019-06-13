#include "motor_driver.h"
#include "ArduinoMotorShieldR3.h"

namespace BioLab
{
    class Motor : public MotorDriver
    {
    public:
        /*
         * @brief Class constructor.
         * @param the DC motor to control
         */
        Motor(MOTOR _motorID): MotorDriver(), motorID(_motorID), motor(), currentRequestedSpeed(0)
        {
          motor.init(); // smells, TODO: refactor
        }

        void setSpeed(int speed)
        {
            currentRequestedSpeed = speed;
            motor.setSpeed(speed, motorID);
        }

        void setBrake(bool state) {
            if (state) {
                setSpeed(0);
            }
            motor.setBrake(state, motorID);
        }

        void setSpeedAndBrake(int speed)
        {
            setBrake(speed == 0);
            setSpeed(speed);
        }

        int getRequestedSpeed() const
        {
            return currentRequestedSpeed;
        }

    private:
        const MOTOR motorID;
        ArduinoMotorShieldR3 motor;
        int currentRequestedSpeed;
    };
};