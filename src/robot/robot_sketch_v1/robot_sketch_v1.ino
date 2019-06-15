#define BT_RX_PIN 16 // A2
#define BT_TX_PIN 17 // A3
#include <SoftwareSerial.h>
SoftwareSerial OtherSerial(BT_RX_PIN, BT_TX_PIN);

#include "logging.h"

#include "robot.h"
BioLab::Robot robot;

void setup()
{
  Serial.begin(9600);
  OtherSerial.begin(9600);
  robot.initialize();
}

void loop()
{
  robot.run();
}
