"""
   /Common/NeurolabSurrogate/NeurolabSurrogate.py
"""

__author__ = 'Nick'

import numpy as np
import pandas as pd
import neurolab as nl
from scipy import stats

class NeurolabSurrogate:
    def __init__(self, trainingFile, inputCols, outputCols, netFile=None):
        '''
        Constructor for NeuroSurrogate, which wraps the neurolab :class:`~neurolab.net.newff` class. This class is a
        feed-forward neural network library written in python. The way this
        differs from the ffnet :mod:`ffnet` feed-forward network library, is that it provides many more types of
        neural networks beyond just the feed-forward case, including :class:`~neurolab.net.newp`,
        :class:`~neurolab.net.newc`, :class:`~neurolab.net.newlvq`, :class:`~neurolab.net.newelm`,
        :class:`~neurolab.net.newhop`, and :class:`~neurolab.net.newhem`. Currently, only support for the
        :class:`~neurolab.net.newff` is supported, but it could easily be extended to those as well.

        :param trainingFile: String location of the training CSV file, which must include column headers
        :param inputCols: List of strings corresponding to the input column names
        :param outputCols: List of strings corresponding to the output column names
        :param netFile: (optional) String location of trained and saved network. This is saved on training \
        completion.
        :return: Initialized NeurolabSurrogate object
        '''

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
        '''
        Neurolab requires that the output data be normalized ahead of time by the user. This can be difficult to deal
        with and makes the library hard to use. This method automates the process of getting the data into the
        correct format then generating a reusable function to convert the data back into the original format after
        you get outputs from the model on calling the sim method.

        :return: normalization function
        '''

        # Get training data to recreate normalization function
        trainData = self.trainData
        outputCols = self.outputCols

        # Use only output columns as input to normalization function
        tar = trainData[outputCols].values
        normf = nl.tool.Norm(tar)
        return normf

    def test(self):
        '''
        Executes the testing of the model with the scipy :func:`~scipy.stats.linregress` function. This prints out
        the results for each output to the console.

        :return: None, prints to console
        '''
        if self.net is not None:
            outNorm = self.net.sim(self.inputData)
            out = self.normf.renorm(outNorm)

            for i, outCol in enumerate(self.outputCols):
                slope, intercept, r_value, p_value, std_err = stats.linregress(self.outputData[:, i].T, out[:,i].T)
                print "Training for " + outCol
                print "slope: " + str(slope)
                print "intercept: " + str(intercept)
                print "r_value: " + str(r_value)
                print "p_value: " + str(p_value)
                print "std_err: " + str(std_err)
                print ""
            return out

    def train(self, num_neurons):
        '''
        Creates a network topology from the num_neurons input, then trains the surrogate model with the initialized \
        input and output data. The network topology is used as an input to the :func:`~neurolab.net.newff`,
        which returns a :class:`~neurolab.core.Net` object.

        :param num_neurons: number of internal neurons :note: this can help create a better fit for a complicated \
        model, at the expense of requiring more computational resources to train.
        :return: None, saves network to disk as neurolabSurrogate.net
        '''

        # Create layers list automatically
        layersList = [num_neurons, len(self.outputCols)]

        # Select only input columns from pandas dataframe as numpy array
        self.inputData = self.trainData[self.inputCols].values
        self.outputData = self.trainData[self.outputCols].values

        # Create feed-forward network
        net = nl.net.newff(nl.tool.minmax(self.inputData), layersList)
        net.train(self.inputData, self.normf(self.outputData), epochs=1000, show=25, goal=0.001)
        self.net = net
        net.save('neurolabSurrogate.net')

    def sim(self, inValue):
        '''
        Executes the trained surrogate model on new input data.

        :param inValue: An array or list of values with the same length of the list of input columns (inputCols)
        :return: An array of values with the same length of the list of output columns (outputCols)
        '''

        # Ensure we already have trained network before trying to sim
        if self.net is not None and len(inValue) == len(self.inputCols):
            inValue = np.asfarray(inValue)
            if inValue.ndim == 0:
                inValue = np.array([[inValue]])  # Neurolab expects 2 dimension array, fix for single value
            if inValue.ndim == 1:
                inValue = np.array([inValue])
            outNorm = self.net.sim(inValue)
            out = self.normf.renorm(outNorm)
            return out[0, 0]
        else:
            raise Exception

    def print_sim(self, inValues):
        '''
        A simple method that wil print out the value of the array, inValues, with the corresponding output value.
        This is primarily used for quickly testing to see how well the trained surrogate works.

        :param inValues: Array or list of input values to retrieve and print out output values for
        :return: None, prints to console
        '''
        for value in inValues:
            print "Input: " + str(value) + " Output: " + str(self.sim(value))