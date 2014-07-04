__author__ = 'Nick'

import scipy.stats as st
import numpy as np
import pandas as pd
from scipy.interpolate import interpolate
import neurolab as nl
import os


class Surrogate:
    def __init__(self, trainingFile, inputCols, outputCols, netFile=None):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.inputCols = inputCols
        self.outputCols = outputCols
        self.trainData = pd.read_csv(self.path + trainingFile)
        self.normf = self.create_norm_function()

        # Load network if we have a saved network file
        if netFile is not None:
            self.net = nl.load(self.path + netFile)
        else:
            pass  # ToDo Add training method to Surrogate class

    def create_norm_function(self):
        # Get training data to recreate normalization function
        trainData = self.trainData
        outputCols = self.outputCols

        # Use only output columns as input to normalization function
        size = trainData.shape[0]
        tar = trainData[outputCols].reshape(size, 1)
        normf = nl.tool.Norm(tar)
        return normf

    def sim(self, inValue):
        inValue = np.asfarray(inValue)
        if inValue.ndim == 0:
            inValue = np.array([[inValue]])  # Neurolab expects 2 dimension array, fix for single value
        outNorm = self.net.sim(inValue)
        out = self.normf.renorm(outNorm)
        return out[0, 0]

    def print_sim(self, inValues):
        for value in inValues:
            print "Input: " + str(value) + " Output: " + str(self.sim(value))


class PedSurrogate:
    def __init__(self, surrogate):
        self.surrogate = surrogate
        self.offDays = 236
        self.onDays = 129

    def sim(self, pedsPerHourOn, pedsPerHourOff):

        avgStepsOn = self.surrogate.sim(pedsPerHourOn)
        avgStepsOff = self.surrogate.sim(pedsPerHourOff)
        
        yearlyStepsPerTile = self.offDays * avgStepsOff + self.onDays * avgStepsOn
        
        return yearlyStepsPerTile

# Only ran when this calc_ped is run directly
# Used for testing the functions
if __name__ == "__main__":
    # Location of training and surrogate files
    trainFile = '\\pedTrainingData.csv'
    netFile = '\\pedSurrogate.net'

    # Load training data and initialize surrogate
    sur = Surrogate(trainingFile=trainFile, inputCols='', outputCols='output', netFile=netFile)

    # Print results of input data
    print "Surrogate Testing Results"
    sur.print_sim(xrange(50, 1500, 100))