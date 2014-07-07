__author__ = 'Nick'

from math import pi

from numba import jit
from math import ceil

@jit
def calc_power(tileCount, pedStepsPerTile, tileEff, tilekWh):
    powerOut = tileCount * pedStepsPerTile * tileEff * tilekWh
    return powerOut


@jit
def calc_cost(tileUnitCost, tileCount, mgtTileUnitCost):

    numMgtTiles = ceil(tileCount / 50)
    return (tileUnitCost * tileCount) + (numMgtTiles * mgtTileUnitCost)
        
