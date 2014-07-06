__author__ = 'Nick'

import numpy as np
import pandas as pd
import neurolab as nl
from scipy import stats
from ffnet import ffnet, mlgraph

class FfnetSurrogate:
    def __init__(self, trainingFile, inputCols, outputCols, netFile=None):

        self.inputCols = inputCols
        self.outputCols = outputCols
        self.trainData = pd.read_csv(trainingFile)
        self.normf = self.create_norm_func()
        self.net = None
        self.inputData = None
        self.outputData = None

        # Load network if we have a saved network file
        if netFile is not None:
            self.net = nl.load(netFile)

    def create_norm_func(self):
        # Get training data to recreate normalization function
        trainData = self.trainData
        outputCols = self.outputCols

        # Use only output columns as input to normalization function
        tar = trainData[outputCols].values
        normf = nl.tool.Norm(tar)
        return normf

    def test(self):
        if self.net is not None:
            out = self.sim(self.inputData)
            #out = self.normf.renorm(outNorm)

            for i, outCol in enumerate(self.outputCols):
                slope, intercept, r_value, p_value, std_err = stats.linregress(self.outputData[:, i].T, out[:,i].T)
                print "Training for " + outCol
                print "slope: " + str(slope)
                print "intercept: " + str(intercept)
                print "r_value: " + str(r_value)
                print "p_value: " + str(p_value)
                print "std_err: " + str(std_err)
                print ""
            #return out

    def train(self, layersList):
        # Select only input columns from pandas dataframe as numpy array
        conec = mlgraph(layersList)
        self.net = ffnet(conec)
        self.inputData = self.trainData[self.inputCols].values
        self.outputData = self.trainData[self.outputCols].values
        self.net.train_tnc(self.inputData, self.outputData, nproc=8, messages=1)
        self.net.test(self.inputData, self.outputData)

    def sim(self, inValue):
        # Ensure we already have trained network before trying to sim
        out = self.net(inValue)
        return out


    def print_sim(self, inValues):
        for value in inValues:
            print "Input: " + str(value) + " Output: " + str(self.sim(value))