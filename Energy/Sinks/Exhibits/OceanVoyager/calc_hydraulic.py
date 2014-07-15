__author__ = 'Nick'

from math import pi

from numba import jit
from Common.FfnetSurrogate.FfnetSurrogate import FfnetSurrogate
import os


def init_protein_skimmer_surrogate():

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

    trainFile = 'hydroProteinTraining.csv'
    netFile = 'trainedProteinSurrogate.net'

    # Get full paths to file co-located with this one
    path = os.path.dirname(os.path.realpath(__file__))
    trainFile = os.path.join(path, trainFile)
    netFile = os.path.join(path, netFile)

    # Load and return stored surrogate object
    return FfnetSurrogate(trainFile, inputCols, outputCols, netFile)

def init_sand_filter_surrogate():

    # Create configuration for surrogate
    inputCols = [
        'pumpFlow',
        'pumpRatedHead',
        'pumpRatedRpm',
        'pumpRunRpm',
        'pumpEff',
        'flowLossCoeff',
        'heatExchFlowLossCoef',
        'heatExchValveOpen',
        'denitFlowLossCoef',
        'ozoneFlowLossCoef',
        'ozoneValveOpen',
        'denitValveOpen',
        'deaerationFlowLossCoef'
    ]

    outputCols = [
        'pumpEffOut',
        'pumpPower',
        'pumpFlow',
        'heatExchFlow1',
        'heatExchFlow2',
        'sandPowerOut',
        'sandPowerIn',
        'sandFlow',
        'heatExchPowerIn',
        'heatExchPowerOut',
        'juncPowerIn',
        'ozone1_6Flow',
        'ozone1_6PowerIn',
        'denitrifictionPowerIn',
        'denitrificationFlow',
        'denitificationPowerOut',
        'ozone7_12Flow',
        'deareationPowerIn',
        'deareationFlow',
        'powerIn',
        'bypassFlow',
        'deareationPowerOut'
    ]

    trainFile = 'hydroSandTraining.csv'
    netFile = 'trainedSandSurrogate.net'

    # Get full paths to file co-located with this one
    path = os.path.dirname(os.path.realpath(__file__))
    trainFile = os.path.join(path, trainFile)
    netFile = os.path.join(path, netFile)

    # Load and return stored surrogate object
    return FfnetSurrogate(trainFile, inputCols, outputCols, netFile)

def calc_protein_power(surrogate, inputs, numPumps):

    outputs = surrogate.sim(inputs)

    totalPower, headOut, totalFlow = calc_protein_power_fast(outputs, numPumps)

    return totalPower, headOut, totalFlow


@jit
def calc_protein_power_fast(outputs, numPumps):
    # total kWh per year
    totalPower = (outputs[0] * numPumps) * 24 * 365

    # head out
    pumpHeadDiff = outputs[5] - outputs[4]
    pumpHeadDiff = pumpHeadDiff * 14.5037738
    headOut = pumpHeadDiff / 0.433

    # total flow out
    totalFlow = outputs[1]
    return totalPower, headOut, totalFlow

def calc_sand_power(surrogate, inputs, numPumps):

    outputs = surrogate.sim(inputs)

    totalPower = (outputs[1] * numPumps) * 24 * 365
    sandFlow = outputs[7]
    heatExchFlow1 = outputs[3]
    heatExchFlow2 = outputs[4]
    denitFlow = outputs[14]
    bypassFlow = outputs[20]
    totalFlow = heatExchFlow2 + denitFlow + bypassFlow + sandFlow

    return totalPower, sandFlow, heatExchFlow1, heatExchFlow2, denitFlow, bypassFlow, totalFlow

@jit
def calc_protein_cost(numPumpRetrofits, pumpModificationUnitCost):
    return numPumpRetrofits * pumpModificationUnitCost


@jit
def calc_sand_cost(numPumpRetrofits, pumpModificationUnitCost):
    return numPumpRetrofits * pumpModificationUnitCost