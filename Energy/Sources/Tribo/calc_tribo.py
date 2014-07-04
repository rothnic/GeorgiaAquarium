__author__ = 'Nick'

from math import pi

from numba import jit


@jit
def calc_power(bladeLength, turbineEff, airDensity, turbineCount, circuitLoss, windData):
    multValue = (0.5 * airDensity * turbineCount * turbineEff * circuitLoss * pi * bladeLength ** 2) / 1000.0
    powerOut = calc_power_fast(windData, multValue, len(windData))

    # sum and return days
    return powerOut


@jit
def calc_power_fast(windData, multValue, theRange):
    """
    Computes the total yearly power for the solar panel system.
    :return: Sum off the power output from each day
    Uses numba just-in-time compilation to LLVM code to speed up the array operation 1000 times.
    """
    sum = 0
    for i in range(theRange):
        sum += (windData[i] ** 3) * multValue
    return sum


@jit
def calc_cost(windCostPerWatt, turbineRating, turbineCount):
    return windCostPerWatt * turbineRating * turbineCount