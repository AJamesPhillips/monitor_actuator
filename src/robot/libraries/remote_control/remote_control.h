/**
 * @file remote_control.h
 * @brief remote control driver definition for the BioLab robot.
 */

namespace BioLab
{
    class RemoteControlDriver
    {
    public:
        /**
          * @brief abstract representation of a remote command.
          */
        struct command_t {
            enum key_t { keyNone, keyF1, keyF2, keyF3, keyF4 };
            int left;   /**< left side speed, between -255 and 255. */
            int right;  /**< right side speed, between -255 and 255. */
            key_t key;  /**< function key. */

            command_t() : left(0), right(0), key(keyNone) {}

            // conversion functions
            void goForward();
            void goBack();
            void turnLeft();
            void turnRight();
            void stop();
            void leftAndRightSliders(int l, int r);
            void forwardBackAndLeftRightSliders(int fb, int lf);
            void joystick(int x, int y);
        };

        /**
          * @brief Class constructor.
          */
        RemoteControlDriver() {}

        /**
         * @brief Return the next remote command, if available.
         * @param cmd a reference to a command_t struct where the command
         *   information will be stored.
         * @return true if a remote command is available, false if not.
         */
        virtual bool getRemoteCommand(command_t& cmd) = 0;
    };
};