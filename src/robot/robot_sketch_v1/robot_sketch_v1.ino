#include "robot.h"

BioLab::Robot robot;

void setup()
{
  Serial.begin(9600);
  Serial.println("BioLab Robot initialize");
  robot.initialize();
}

void loop()
{
  robot.run();
}
