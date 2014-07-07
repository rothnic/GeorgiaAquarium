__author__ = 'Nick'

from math import pi

from numba import jit
from Common.FfnetSurrogate.FfnetSurrogate import FfnetSurrogate
import os


def init_surrogate():

    # Create configuration for surrogate
    inputCols = [
        "ratedSpeed",
        "flc",
        "ratedEff",
        "ratedHead",
        "ratedFlow",
        "csa",
        "runSpeed"
    ]

    outputCols = [
        "pumpHp",
        "totalFlowOut",
        "pskFlow2",
        "pskFlow1",
        "pIn",
        "pOut1"
    ]

    trainFile = 'hydroTraining.csv'
    netFile = 'trainedHydroSurrogate.net'

    # Get full paths to file co-located with this one
    path = os.path.dirname(os.path.realpath(__file__))
    trainFile = os.path.join(path, trainFile)
    netFile = os.path.join(path, netFile)

    # Load and return stored surrogate object
    return FfnetSurrogate(trainFile, inputCols, outputCols, netFile)


def calc_power(surrogate, inputs, numPumps):

    outputs = surrogate.sim(inputs)

    totalPower, headOut, totalFlow = calc_power_fast(outputs, numPumps)

    return totalPower, headOut, totalFlow


@jit
def calc_power_fast(outputs, numPumps):
    # total kWh per year
    totalPower = (outputs[0] * numPumps) * 24 * 365

    # head out
    pumpHeadDiff = outputs[5] - outputs[4]
    pumpHeadDiff = pumpHeadDiff * 14.5037738
    headOut = pumpHeadDiff / 0.433

    # total flow out
    totalFlow = outputs[1]
    return totalPower, headOut, totalFlow


@jit
def calc_cost():
    return 119000.0