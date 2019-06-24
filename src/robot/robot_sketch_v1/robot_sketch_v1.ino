#define BT_RX_PIN 16 // A2
#define BT_TX_PIN 17 // A3
#include <SoftwareSerial.h>
SoftwareSerial OtherSerial(BT_RX_PIN, BT_TX_PIN);

#include "logging.h"

#include "robot.h"
BioLab::Robot robot;

enum class COMMAND {
  Move
};

const unsigned int BAUD_RATE = 9600; // 38400; // 57600;
float waitForNewActivityUntil = 1000;

String partialString = "";
unsigned long lastActivityAt = 0;

void handleCommand (String command)
{
  if (command.startsWith("move%"))
  {
    int leftMotorPower = 140;
    unsigned long leftMotorDuration = 1000;
    int rightMotorPower = 140;
    unsigned long rightMotorDuration = 500;

    robot.move(BioLab::RobotMotor::Left, leftMotorPower, leftMotorDuration);
    robot.move(BioLab::RobotMotor::Right, rightMotorPower, rightMotorDuration);
  }
  else
  {
    OtherSerial.println(String("Unknown command: ") + command);
  }
}

void handleCharacter (char character)
{
  partialString += character;
  lastActivityAt = millis();

  if (character == 'S')
  {
    int endIndex = partialString.length() - 1;
    String command = partialString.substring(1, endIndex);
    handleCommand(command);
    OtherSerial.println(String("Handled command: ") + command);
    partialString = "";
  }
}

void setup()
{
  Serial.begin(9600);
  OtherSerial.begin(BAUD_RATE);
  OtherSerial.println("Hello world");
  robot.initialize();
}

void loop()
{
  if (OtherSerial.available())
  {
    char character = OtherSerial.read();
    handleCharacter(character);
  }
  else
  {
    unsigned long diff = millis() - lastActivityAt;
    if (diff > waitForNewActivityUntil)
    {
      OtherSerial.println("HB");
      lastActivityAt = millis();
    }
  }

  robot.update();
}
