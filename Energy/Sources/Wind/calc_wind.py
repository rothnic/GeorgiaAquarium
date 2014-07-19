__author__ = 'Nick'

from math import pi

from numba import jit


#@jit
def calc_power(bladeLength, turbineEff, airDensity, turbineCount, circuitLoss, windData):
    '''
    http://en.wikipedia.org/wiki/Density_of_air
    http://www.raeng.org.uk/education/diploma/maths/pdf/exemplars_advanced/23_Wind_Turbine.pdf
    power = 1/2 (air density) (wind speed in m/sec)^3 ( pi*(blade length)^2) * C
    C = power efficiency (0.35 to 0.45, theoretical max at 0.59)
    (air density) = (absolute pressure) / (R * T)
    R = 287.058J/(kgK)
    T = absolute temperature

    :param windSpeed:
    :param bladeLength: meters
    :param turbineEff:
    :param airDensity:
    :return:

    '''
    powerMult = (0.5 * airDensity * turbineCount * turbineEff * circuitLoss * pi * (bladeLength ** 2)) / 1000.0
    powerOut = calc_power_fast(windData, powerMult, len(windData))

    # sum and return days
    return powerOut


#@jit
def calc_power_fast(windData, powerMult, theRange):
    '''
    Computes the total yearly power for the solar panel system. :Note: Uses numba just-in-time compilation to LLVM code
    to speed up the array operation 1000 times.

    :param windData: Numpy array of wind on a daily basis
    :param powerMult: Power factor multiplier from :func:`~Energy.Sources.Wind.calc_wind.calc_power`
    :param theRange: Size of the array, so we can avoid using Python objects and ensure function compiles to LLVM
    :return: Sum off the power output from each day for one year
    '''
    sum = 0
    for i in range(theRange):
        sum += (windData[i] ** 3) * powerMult
    return sum


#@jit
def calc_cost(windCostPerWatt, turbineRating, turbineCount):
    return windCostPerWatt * turbineRating * turbineCount