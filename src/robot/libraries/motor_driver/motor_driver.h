
namespace BioLab
{
    class MotorDriver
    {
    public:
        /**
         * @brief Change the speed of the motor.
         * @param speed The new speed of the motor.
         *  Valid values are between -255 and 255.
         *  Use positive values to run the motor forward,
         *  negative values to run it backward,
         *  and zero to stop the motor (but not to put break on).
         */
        virtual void setSpeed(int speed) = 0;

        virtual void setBrake(bool state) = 0;

        virtual void setSpeedAndBrake(int speed) = 0;

        /**
         * @brief Return the current requested speed of the motor.
         * @return The current speed of the motor with range -255 to 255.
         */
        virtual int getRequestedSpeed() const = 0;
    };
};
