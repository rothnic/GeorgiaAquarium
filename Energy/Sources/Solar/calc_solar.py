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


def load_solar_data(fullFile):
    pass