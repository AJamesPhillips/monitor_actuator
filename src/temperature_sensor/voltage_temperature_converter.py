
from .characterise_thermistor import C_TO_KELVIN, resistance_to_temperature_kelvin


def make_voltage_to_temperature_converter(total_voltage, constant_resistance, a, b, c):
    # From characterise_thermistor.py
    def converter(voltage_accross_thermistor):
        Vat = voltage_accross_thermistor
        Vt = total_voltage
        # Rt = thermistor_resistance
        Rc = constant_resistance
        # Using the voltage divider equation:
        #    Vat = Vt * (Rt / (Rt + Rc))
        #    (Vat / Vt) = Rt / (Rt + Rc)
        #    (Vat / Vt) * (Rt + Rc) = Rt
        #    (Vat / Vt) * Rt + (Vat / Vt) * Rc = Rt
        #    (Vat / Vt) * Rc = Rt - (Vat / Vt) * Rt
        #    (Vat / Vt) * Rc = Rt * (1 - (Vat / Vt))
        #    Rt = ((Vat / Vt) * Rc) / (1 - (Vat / Vt))

        thermistor_resistance = ((Vat / Vt) * Rc) / (1 - (Vat / Vt))

        # assert 0

        return resistance_to_temperature_kelvin(thermistor_resistance, a, b, c) - C_TO_KELVIN
    return converter


therm01_in_adc__2017_01_31__parameters = {
    # TODO, electrical implementation should use a voltage reference
    'total_voltage': 5.0,
    'constant_resistance': 9400,
    # From characterise_thermistor.py using Steinhart-Hart_equation
    'a': -42955.23867929,
    'b':  9451.05880751,
    'c': -66.85765313,
}

convert_therm01_in_adc__2017_01_31__voltage_to_temp = make_voltage_to_temperature_converter(**therm01_in_adc__2017_01_31__parameters)
