__author__ = 'Nick'

from math import pi

from numba import jit


@jit
def calc_power(tileCount, pedStepsPerTile, tileEff, tilekWh):
    powerOut = tileCount * pedStepsPerTile * tileEff * tilekWh
    return powerOut


@jit
def calc_cost(tileUnitCost, tileCount, mgtTileUnitCost):
    if tileCount <= 50
        return tileUnitCost * tileCount + mgtTileUnitCost
    else
        numMgtTiles = int(tileCount / 50)
        if tileCount mod 50 > 0
            numMgtTiles = numMgtTiles + 1
        return (tileUnitCost * tileCount) + (numMgtTiles * mgtTileUnitCost)
        
