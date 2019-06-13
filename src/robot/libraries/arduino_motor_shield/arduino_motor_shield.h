#include "motor_driver.h"
#include "ArduinoMotorShieldR3.h"

namespace BioLab
{
    class Motor : public MotorDriver
    {
    public:
        Motor(MOTOR _motorID);

        void setSpeed(int speed);
        void setBrake(bool state);
        void setSpeedAndBrake(int speed);
        int getRequestedSpeed() const;

    private:
        const MOTOR motorID;
        ArduinoMotorShieldR3 motor;
        int currentRequestedSpeed;
    };
};
