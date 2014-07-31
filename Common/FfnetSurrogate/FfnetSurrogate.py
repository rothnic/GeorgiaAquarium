"""
   /Common/FfnetSurrogate/FfnetSurrogate.py
"""

__author__ = 'Nick'

import pandas as pd
from scipy import stats
from ffnet import ffnet, mlgraph, imlgraph, savenet, loadnet

class FfnetSurrogate:
    def __init__(self, trainingFile, inputCols, outputCols, netFile=None, multi=False):
        '''
        Constructor for FfnetSurrogate, which wraps the ffnet :class:`~ffnet.ffnet` class. This class is a
        feed-forward neural network library written in Fortran, that is wrapped with a python interface. The way this
        differs from the neurolab :class:`~neurolab.net.newff` feed-forward network class, is that it can make use of
        multiple processors for training, and typically produces better results.

        There is an existing plugin for OpenMDAO wrapping this library, but using it involves actually having the
        real model connected into OpenMDAO for training. This class provides the ability to just have a csv file of
        results, so that you can generate the surrogate ahead of time, then just use it by loading the saved model.

        :param trainingFile: String location of the training CSV file, which must include column headers
        :param inputCols: List of strings corresponding to the input column names
        :param outputCols: List of strings corresponding to the output column names
        :param regressorFile: (optional) String location of trained and saved network. This is saved on training \
        completion.
        :return: Initialized FfnetSurrogate object
        '''

        self.inputCols = inputCols
        self.outputCols = outputCols
        self.trainData = pd.read_csv(trainingFile)
        self.net = None
        self.inputData = None
        self.outputData = None

        # Load network if we have a saved network file
        if netFile is not None:
            self.net = loadnet(netFile)

    def test(self):
        '''
        Executes the testing of the model with the scipy :func:`~scipy.stats.linregress` function. This prints out
        the results for each output to the console.

        :return: None, prints to console
        '''
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

    def train(self, num_neurons):
        '''
        Creates a network topology from the num_neurons input, then trains the surrogate model with the initialized \
        input and output data. The network topology is used as an input to the :class:`~ffnet.ffnet` initializer.

        :param num_neurons: number of internal neurons :note: this can help create a better fit for a complicated \
        model, at the expense of requiring more computational resources to train.
        :return: None, saves network to disk as ffnetSurrogate.net
        '''

        # Select only input columns from pandas dataframe as numpy array
        layersList = [len(self.inputCols), num_neurons, len(self.outputCols)]
        conec = mlgraph(layersList)
        self.net = ffnet(conec)
        self.inputData = self.trainData[self.inputCols].values
        self.outputData = self.trainData[self.outputCols].values
        self.net.train_tnc(self.inputData, self.outputData, nproc='ncpu', messages=1)
        self.net.test(self.inputData, self.outputData)

        # Save the trained network to disk

        savenet(self.net, 'ffnetSurrogate.net')

    def sim(self, inValue):
        '''
        Executes the trained surrogate model on new input data.

        :param inValue: An array or list of values with the same length of the list of input columns (inputCols)
        :return: An array of values with the same length of the list of output columns (outputCols)
        '''

        # Ensure we already have trained network before trying to sim
        out = self.net(inValue)
        return out

    def print_sim(self, inValues):
        '''
        A simple method that wil print out the value of the array, inValues, with the corresponding output value.
        This is primarily used for quickly testing to see how well the trained surrogate works.

        :param inValues: Array or list of input values to retrieve and print out output values for
        :return: None, prints to console
        '''
        for value in inValues:
            print "Input: " + str(value) + " Output: " + str(self.sim(value))