#!/usr/bin/python3
# Fit the temperature and resistance

import numpy as np


# Resistances and temperatures recorded in August from the grey "French" thermistor
resistances__therm01__2016_08 = [1026, 1004, 972, 959, 941, 906, 882, 858, 833]
temperature__therm01__2016_08 = [29.2, 26.2, 22.6, 20.2, 18, 13.1, 9.7, 6.1, 1.2]
resistances__therm01_in_adc__2017_01_31 = [899, 906, 921, 927, 931]
temperature__therm01_in_adc__2017_01_31 = [16.8, 18.2, 20.2, 20.8, 21.3]
C_TO_KELVIN = 273.15


def resistance_to_temperature_kelvin(thermistor_resistance, a, b, c): #, d, e):
    x = thermistor_resistance

    # equation1
    # return np.multiply(a, x) + np.multiply(b, np.power(x, c)) + np.multiply(d, np.power(x, e))

    # equation2
    # return a * np.log(x + b) + c

    # Using the Steinhart-Hart_equation https://en.wikipedia.org/wiki/Thermistor#Steinhart.E2.80.93Hart_equation
    # Don't understand why it's not 1/T but whatever, looks like we get a good fit
    return (a + b * np.log(x) + c * (np.log(x))**3 )


def characterise(resistances, temperatures):
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit

    absolute_temperatures = np.array(temperatures) + C_TO_KELVIN

    parameter, covariance_matrix = curve_fit(resistance_to_temperature_kelvin, resistances, absolute_temperatures)

    plt.plot(resistances, absolute_temperatures, 'rx', label='data')
    plt.plot(resistances, resistance_to_temperature_kelvin(resistances, *parameter), 'b-', label='fit')
    plt.show()

    print(parameter)


if __name__ == '__main__':
    # # parameter has the following values:
    # # [72.91140136, -411.96050326, -439.08254886]  # equation 2
    # # [-2161.21683309   472.21473306    -2.43223168]  # Steinhart-Hart_equation
    # characterise(resistances__therm01__2016_08, temperature__therm01__2016_08)

    # parameters are:
    # [-42955.23867929   9451.05880751    -66.85765313]
    characterise(resistances__therm01_in_adc__2017_01_31, temperature__therm01_in_adc__2017_01_31)
