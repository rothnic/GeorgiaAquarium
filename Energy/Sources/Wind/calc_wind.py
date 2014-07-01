__author__ = 'Nick'

from math import ceil, pi

from numba import jit


@jit
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
    multValue = (0.5 * airDensity * turbineCount * turbineEff * circuitLoss * pi * bladeLength ** 2)/1000.0
    powerOut = calc_power_fast(windData, multValue, len(windData))

    # sum and return days
    return powerOut


@jit
def calc_power_fast(windData, multValue, theRange):
    '''
    Computes the total yearly power for the solar panel system.

    :return: Sum off the power output from each day

    Uses numba just-in-time compilation to LLVM code to speed up the array operation 1000 times.
    '''
    sum = 0
    for i in range(theRange):
        sum += (windData[i] ** 3) * multValue
    return sum


@jit
def calc_cost(windCostPerWatt, turbineRating, turbineCount):
    return windCostPerWatt * turbineRating * turbineCount