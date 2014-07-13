__author__ = 'Nick'

import pandas as pd
from scipy import stats
from ffnet import ffnet, mlgraph, imlgraph, savenet, loadnet


class FfnetSurrogate:
    def __init__(self, trainingFile, inputCols, outputCols, netFile=None):

        self.inputCols = inputCols
        self.outputCols = outputCols
        self.trainData = pd.read_csv(trainingFile)
        self.net = None
        self.inputData = None
        self.outputData = None

        # Load network if we have a saved network file
        if netFile is not None:
            self.load(netFile)

    def test(self):
        if self.net is not None:
            out = self.sim(self.inputData)
            for i, outCol in enumerate(self.outputCols):
                slope, intercept, r_value, p_value, std_err = stats.linregress(self.outputData[:, i].T, out[:, i].T)
                print "Training for " + outCol
                print "slope: " + str(slope)
                print "intercept: " + str(intercept)
                print "r_value: " + str(r_value)
                print "p_value: " + str(p_value)
                print "std_err: " + str(std_err)
                print ""

    def train(self, layersList):
        # Select only input columns from pandas dataframe as numpy array
        conec = mlgraph(layersList)
        self.net = ffnet(conec)
        self.inputData = self.trainData[self.inputCols].values
        self.outputData = self.trainData[self.outputCols].values
        self.net.train_tnc(self.inputData, self.outputData, nproc='ncpu', messages=1)
        #self.net.train_genetic(self.inputData, self.outputData, verbosity=1)
        self.net.test(self.inputData, self.outputData)

    def sim(self, inValue):
        # Ensure we already have trained network before trying to sim
        out = self.net(inValue)
        return out

    def save(self, filename):
        savenet(self.net, filename)

    def load(self, filename):
        self.net = loadnet(filename)

    def print_sim(self, inValues):
        for value in inValues:
            print "Input: " + str(value) + " Output: " + str(self.sim(value))