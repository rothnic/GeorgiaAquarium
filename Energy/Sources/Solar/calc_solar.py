__author__ = 'Nick'

from math import ceil

from numba import jit


@jit
def calc_power(panelRating, panelEff, sunRadianceScalar, surfaceArea, circuitLoss, sunData):
    multValue = (surfaceArea * panelEff * circuitLoss) / 1000.0
    powerOut = calc_power_fast(sunData, multValue, len(sunData))

    # sum and return days
    return powerOut


@jit
def calc_power_fast(sunData, multValue, theRange):
    '''
    Computes the total yearly power for the solar panel system.

    :param sunData: The solar irradiance array for one year
    :param multValue: The value to multiply each value in the array by
    :param theRange: Length of the input array, input to avoid JIT compilation issues
    :return: Sum off the power output from each day

    Uses numba just-in-time compilation to LLVM code to speed up the array operation 1000 times.
    '''
    sum = 0
    for i in range(theRange):
        sum += sunData[i] * multValue
    return sum


@jit
def calc_cost(solarCostPerWatt, panelRating, numPanels):

    return solarCostPerWatt * numPanels * panelRating

@jit
def calc_num_panels(surfaceArea, panelSize):
    return ceil(surfaceArea / panelSize)