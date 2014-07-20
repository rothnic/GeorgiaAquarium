__author__ = 'Nick'

from math import ceil

from numba import jit


#@jit
def calc_power(tileCount, pedStepsPerTile, tileEff, tilekWh):
    '''
    Calc_power computes the total number of steps that will occur across all tiles for this given design
    configuration. The total number of steps is affected by the number of tiles and the pedestrian model that
    simulates both on and off season steps per tile.

    :param tileCount: A design variable for how many tiles you would want to purchase
    :param pedStepsPerTile: An uncertainty for the number of expected steps per tile over a year
    :param tileEff: The amount of actual useful energy based on the claimed
    :param tilekWh: The claimed power return when one person steps on a tile
    :return: The total energy generated in a year for the input design configuration
    '''
    return tileCount * pedStepsPerTile * tileEff * tilekWh


#@jit
def calc_cost(tileUnitCost, tileCount, mgtTileUnitCost):
    '''
    Calc_cost computes the cost of a triboelectric system based on the PedGen pricing model. There are affects to
    cost based on the number of units you purchase, which affects how many management tiles are needed as well.

    :param tileUnitCost: A cost per regular tile type when purchased in bulk
    :param tileCount: The whole number count of tiles to be installed
    :param mgtTileUnitCost: The cost per management tile
    :return: The cost of purchasing and installation of the tribo system
    '''

    # Get number of times
    numMgtTiles = ceil(tileCount / 50)

    # Change pricing factor based on number of tiles
    if tileCount < 100:
        tileUnitCost = tileUnitCost * 1.5

    return (tileUnitCost * tileCount) + (numMgtTiles * mgtTileUnitCost)
        
