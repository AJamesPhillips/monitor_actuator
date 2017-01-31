
from src.temperature_sensor.voltage_temperature_converter import convert_therm01_in_adc__2017_01_31__voltage_to_temp

def test_convert_channel1_voltage_to_temp():
    temp = convert_therm01_in_adc__2017_01_31__voltage_to_temp(0.436788)
    temp = round(temp * 100) / 100
    assert(17.0 == temp)
