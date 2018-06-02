
# Temperature logger

## Implementations

### Option 1: ADC

Built for raspberry pi zero with [ADC board from ABElectronics](https://www.abelectronics.co.uk/p/69/ADC-Pi-Zero-Raspberry-Pi-Analogue-to-Digital-converter)
5V from board Vcc used in voltage divider with 9.4 k ohm and the thermister.
TODO, electrical implementation should use a voltage reference instead of 5V
from the board and or use a Wheatstone bridge.

### Option 2: Digital DS18B20

1-Wire DS18B20
Buy from ebay, £11 for 5: [5pcs DS18b20 Waterproof Temperature Sensor Thermal Probe Thermometer Durable 2M](http://www.ebay.co.uk/itm/162158276878)
Using these instructions:
Wire up:

    * RED=Vcc (5V supply)
    * BLACK=GND
    * WHITE/YELLOW=SIG (GPIO4)
    * 4.7 kOhm "pull-up" resistor between yellow (SIG) and red (Vcc)
