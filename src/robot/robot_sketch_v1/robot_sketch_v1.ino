#define BT_RX_PIN 16 // A2
#define BT_TX_PIN 17 // A3
#include <SoftwareSerial.h>
SoftwareSerial OtherSerial(BT_RX_PIN, BT_TX_PIN);

#include "logging.h"

#include "robot.h"
BioLab::Robot robot;

enum class CYCLE {
  ChangeCommand,
  StoreThenEcho,
  EchoChar
};

const unsigned int BAUD_RATE = 9600; // 57600;
// const unsigned int BITS_PER_CHARACTER = 10;
// const float CHARACTERS_PER_SECOND = float(BAUD_RATE) / float(BITS_PER_CHARACTER);
// const float MS_PER_CHARACTER = 1000.0 / CHARACTERS_PER_SECOND;
float waitForNewCharacterUntil = 100; // MS_PER_CHARACTER * 3;

String partialString = "";

CYCLE cycle = CYCLE::StoreThenEcho;
unsigned long lastCharReceivedAt = 0;

int prefixLength = 0;

String cycleToString (CYCLE cycle)
{
  if (cycle == CYCLE::ChangeCommand)
  {
    return "ChangeCommand";
  }
  else if (cycle == CYCLE::StoreThenEcho)
  {
    return "StoreThenEcho";
  }
  else if (cycle == CYCLE::EchoChar)
  {
    return "EchoChar";
  }

  return "Undefined";
}

void changeCommand (String command)
{
  if (command == "storethenecho")
  {
    cycle = CYCLE::StoreThenEcho;
    OtherSerial.println(String("cycle changed to ") + cycleToString(cycle));
  }
  else if (command == "echochar")
  {
    cycle = CYCLE::EchoChar;
    OtherSerial.println(String("cycle changed to ") + cycleToString(cycle));
  }
  else if (command.startsWith("prefixlength"))
  {
    command.replace("prefixlength", "");
    prefixLength = command.toInt();
    OtherSerial.println(String("prefixLength changed to: ") + String(prefixLength));
  }
}

void handleCharacter (char character)
{
  if (character == 'C')
  {
    // Change command
    cycle = CYCLE::ChangeCommand;
    OtherSerial.println(String("cycle changed to ") + cycleToString(cycle));
  }

  partialString += character;
  lastCharReceivedAt = millis();

  if (cycle == CYCLE::ChangeCommand)
  {
    if (character == 'S')
    {
      int endIndex = partialString.length() - 1;
      String command = partialString.substring(1, endIndex);
      changeCommand(command);
    }
  }
  else if (cycle == CYCLE::StoreThenEcho)
  {
    // do nothing else yet
  }
  else if (cycle == CYCLE::EchoChar)
  {
    String prefixString = "AAAAAAAAAABBBBBBBBB\nAAAAAAAAAABBBBBBBBB\nAAAAAAAAAABBBBBBBBB\n";
    prefixString = prefixString.substring(0, prefixLength);
    prefixString += character;
    OtherSerial.println(prefixString);
  }
}

void setup()
{
  Serial.begin(9600);
  OtherSerial.begin(BAUD_RATE);
  OtherSerial.println("Hello, world?");
  robot.initialize();
}

void loop()
{
  if (OtherSerial.available())
  {
    char character = OtherSerial.read();
    handleCharacter(character);
  } else
  {
    if (partialString != "")
    {
      unsigned long diff = millis() - lastCharReceivedAt;
      // Wait for more than enough time between characters
      if (diff > waitForNewCharacterUntil)
      {
        if (cycle == CYCLE::StoreThenEcho)
        {
          partialString = "partialString: " + partialString;
          OtherSerial.println(partialString);
        }

        partialString = "";
        OtherSerial.println("R"); // Ready for next message
      }
    }
  }
}
