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
  // Example: Cmove%L-120_0000_R+120_2000%S
  // Move Left power = -120 duration = 0 (indefinite)
  // Move Right power = 120 duration = 2000
  if (command.startsWith("move%"))
  {
    String parameters = command.substring(5);
    while (parameters.length() > 0)
    {
      bool leftMotor = parameters.startsWith("L");
      parameters = parameters.substring(1);
      int power = parameters.substring(0, 4).toInt();
      parameters = parameters.substring(5);
      unsigned long duration = parameters.substring(0, 4).toInt();
      parameters = parameters.substring(5);

      // OtherSerial.println(String("Move Left: ") + String(leftMotor) + String(" power = ") + String(power) + String(" duration = " + String(duration)));
      if (leftMotor)
      {
        robot.move(BioLab::RobotMotor::Left, power, duration);
      }
      else
      {
        robot.move(BioLab::RobotMotor::Right, power, duration);
      }
    }
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
    int endIndex = partialString.length() - 2;
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
