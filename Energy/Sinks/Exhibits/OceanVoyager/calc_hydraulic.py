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

    totalPower, headOut, totalFlow, proteinPumpPower = calc_protein_power_fast(outputs, numPumps)

    return totalPower, headOut, totalFlow, proteinPumpPower


#@jit
def calc_protein_power_fast(outputs, numPumps):
    # total kWh per year
    proteinPumpPower = outputs[0]
    totalPower = (proteinPumpPower * numPumps) * 24 * 365

    # head out
    pumpHeadDiff = outputs[5] - outputs[4]
    pumpHeadDiff = pumpHeadDiff * 14.5037738
    headOut = pumpHeadDiff / 0.433

    # total flow out
    totalFlow = outputs[1]
    return totalPower, headOut, totalFlow, proteinPumpPower


def calc_sand_power(surrogate, inputs, numPumps):

    outputs = surrogate.sim(inputs)

    totalPower = (outputs[1] * numPumps) * 24 * 365
    sandFlow = -outputs[7]
    heatExchFlow1 = outputs[3]
    heatExchFlow2 = -outputs[4]
    denitFlow = -outputs[14]
    bypassFlow = -outputs[20]
    totalFlow = heatExchFlow2 + denitFlow + bypassFlow + sandFlow

    return totalPower, sandFlow, heatExchFlow1, heatExchFlow2, denitFlow, bypassFlow, totalFlow


#@jit
def calc_protein_cost(numPumpRetrofits, pumpModificationUnitCost, lossMultiplier, currentProteinCircuitLoss,
                      proteinRatedEff, currentProteinRatedEff, proteinRatedSpeed, currentProteinRatedSpeed,
                      ratedFlow, currentProteinRatedFlow, ratedHead, currentProteinRatedHead):

    # Cost depends on whether we have changed the configuration of the system
    if (currentProteinRatedSpeed == proteinRatedSpeed and currentProteinRatedFlow == ratedFlow and
                currentProteinRatedEff == proteinRatedEff and currentProteinRatedHead == ratedHead and
                currentProteinCircuitLoss == lossMultiplier):
        # Cost is nothing if we don't change the system
        return 0.0
    else:
        effDiff = max(proteinRatedEff*100 - currentProteinRatedEff, 0)
        headDiff = max(ratedHead - currentProteinRatedHead, 0)
        lossDiff = abs(min((lossMultiplier - currentProteinCircuitLoss)/currentProteinCircuitLoss, 0))
        effCostFactor = 4500 * effDiff
        headCostFactor = 400 * headDiff
        lossCostFactor = 200000 * lossDiff
        return (numPumpRetrofits * pumpModificationUnitCost) + effCostFactor + headCostFactor + lossCostFactor


#@jit
def calc_sand_cost(numPumpRetrofits, pumpModificationUnitCost, pumpRatedRpm, currentSandRatedSpeed,
                    pumpFlow, currentSandRatedFlow, pumpEff, currentSandRatedEff,
                    pumpRatedHead, currentSandRatedHead, flowLossCoef, currentSandCircuitLoss,
                    heatExchFlowLossCoef, currentSandHxCircuitLoss, ozoneFlowLossCoef, currentSandOzCircuitLoss,
                    denitFLowLossCoef, currentSandDnCircuitLoss, deaerationFlowLossCoef, currentSandDatCircuitLoss):

    # Cost depends on whether we have changed the configuration of the system
    if (pumpRatedRpm == currentSandRatedSpeed and pumpFlow == currentSandRatedFlow and
                pumpEff == currentSandRatedEff and pumpRatedHead == currentSandRatedHead):
        return 0.0
    else:
        effDiff = max(pumpEff*100 - currentSandRatedEff, 0)
        headDiff = max(pumpRatedHead - currentSandRatedHead, 0)
        lossDiff = abs(min((flowLossCoef - currentSandCircuitLoss) / currentSandCircuitLoss, 0))
        hxLossDiff = abs(min((heatExchFlowLossCoef - currentSandHxCircuitLoss) / currentSandHxCircuitLoss, 0))
        ozLossDiff = abs(min((ozoneFlowLossCoef - currentSandOzCircuitLoss) / currentSandOzCircuitLoss, 0))
        dnLossDiff = abs(min(((denitFLowLossCoef - currentSandDnCircuitLoss) / currentSandDnCircuitLoss, 0)))
        datLossDiff = abs(min((deaerationFlowLossCoef - currentSandDatCircuitLoss) / currentSandDatCircuitLoss, 0))
        effCostFactor = 4500 * effDiff
        headCostFactor = 400 * headDiff
        lossCostFactor = 200000 * lossDiff
        heatExchCostFactor = 200000 * hxLossDiff
        ozLossFactor = 200000 * ozLossDiff
        dnLossFactor = 200000 * dnLossDiff
        datLossDiff = 200000 * datLossDiff

        return (numPumpRetrofits * pumpModificationUnitCost) + effCostFactor + headCostFactor + lossCostFactor \
            + heatExchCostFactor + ozLossFactor + dnLossFactor + datLossDiff