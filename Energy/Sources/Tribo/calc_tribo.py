__author__ = 'Nick'

from math import pi

from numba import jit


@jit
def calc_power(tileCount, pedStepsPerTile, triboEff, tribokWh):
    powerOut = tileCount * pedStepsPerTile * triboEff * tribokWh
    return powerOut


@jit
def calc_cost(triboUnitCost, tileCount):
    return triboUnitCost * tileCount