#!/usr/bin/python3
# Fit the temperature and resistance

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# Resistances and temperatures recorded in August from the grey "French" thermistor
x_resistance = [1026, 1004, 972, 959, 941, 906, 882, 858, 833]
y_temperature = [29.2, 26.2, 22.6, 20.2, 18, 13.1, 9.7, 6.1, 1.2]
C_TO_KELVIN = 273.15
y_temperature_absolute = np.array(y_temperature) + C_TO_KELVIN


def resistance_to_temperature_kelvin(thermistor_resistance, a, b, c): #, d, e):
    x = thermistor_resistance

    # equation1
    # return np.multiply(a, x) + np.multiply(b, np.power(x, c)) + np.multiply(d, np.power(x, e))

    # equation2
    # return a * np.log(x + b) + c

    # Using the Steinhart-Hart_equation https://en.wikipedia.org/wiki/Thermistor#Steinhart.E2.80.93Hart_equation
    # Don't understand why it's not 1/T but whatever, looks like we get a good fit
    return (a + b * np.log(x) + c * (np.log(x))**3 )


def main():
    parameter, covariance_matrix = curve_fit(resistance_to_temperature_kelvin, x_resistance, y_temperature_absolute)

    plt.plot(x_resistance, y_temperature_absolute, 'rx', label='data')
    plt.plot(x_resistance, resistance_to_temperature_kelvin(x_resistance, *parameter), 'b-', label='fit')
    plt.show()

    # parameter has the following values:
    # [72.91140136, -411.96050326, -439.08254886]  # equation 2
    # [-2161.21683309   472.21473306    -2.43223168]  # Steinhart-Hart_equation
    print(parameter)


if __name__ == '__main__':
    main()
