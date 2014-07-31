"""
   /Common/DecisionTreeSurrogate/DecisionTreeSurrogate.py
"""

__author__ = 'Nick'

import cPickle as cpkl

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestRegressor


class DecisionTreeSurrogate:
    def __init__(self, trainingFile, inputCols, outputCols, regressorFile=None):
        '''
        Constructor for DecisionTreeSurrogate, which wraps the scikit-learn
        :class:`~sklearn.ensemble.RandomForestRegressor` class. This class generates many dicision trees with random
        configurations to avoid overfitting the model to the training data.

        :param trainingFile: String location of the training CSV file, which must include column headers
        :param inputCols: List of strings corresponding to the input column names
        :param outputCols: List of strings corresponding to the output column names
        :param regressorFile: (optional) String location of trained and pickled model. This is saved on training \
        completion.
        :return: Initialized DecisionTreeSurrogate object
        '''

        self.inputCols = inputCols
        self.outputCols = outputCols
        self.trainData = pd.read_csv(trainingFile)
        self.regressor = None
        self.inputData = None
        self.outputData = None

        # Load regressor if we have a saved regressor file
        if regressorFile is not None:
            with open(regressorFile, 'rb') as handle:
                self.regressor = cpkl.load(handle)

    def test(self):
        '''
        Executes the testing of the model with the scipy :func:`~scipy.stats.linregress` function. This prints out
        the results for each output to the console.

        :return: None, prints to console
        '''
        # ToDo: determine why cross_val_score fails when testing surrogate model (see commented out code)

        if self.regressor is not None:
            out = self.regressor.predict(self.inputData)
            # scores = cross_val_score(self.regressor, self.inputData, self.outputData, cv=20, scoring='r2')
            # print "Cross Validation for Trained Model"
            # print "Mean: " + str(scores.mean())
            # print "Std: " + str(scores.std()*2)
            # print ""
            for i, outCol in enumerate(self.outputCols):
                if out.ndim == 1:
                    out = np.asarray(out).reshape(out.size, 1)
                slope, intercept, r_value, p_value, std_err = stats.linregress(self.outputData[:, i], out[:, i])
                print "Training for " + outCol
                print "slope: " + str(slope)
                print "intercept: " + str(intercept)
                print "r_value: " + str(r_value)
                print "p_value: " + str(p_value)
                print "std_err: " + str(std_err)
                print ""
            return out

    def train(self, n_estimators):
        '''
        Trains the surrogate model with the initialized input and output data, given the number of estimators to use.
        This is used as an input to the :class:`~sklearn.ensemble.RandomForestRegressor` initializer, and controls
        the number of decision trees created by the random forest tree.

        :param n_estimators: number of decision trees for training, :note: can increase run time
        :return: None
        '''
        # Select only input columns from pandas dataframe as numpy array
        self.inputData = self.trainData[self.inputCols].values
        self.outputData = self.trainData[self.outputCols].values

        # Create decision tree regressor object
        self.regressor = RandomForestRegressor(n_estimators=n_estimators, n_jobs=-1)

        # Fit regressor to inputs/outputs
        self.regressor.fit(self.inputData, self.outputData)

        with open("decisionTreeSurrogate.p", "wb") as handle:
            cpkl.dump(self.regressor, handle)

    def sim(self, inValue):
        '''
        Executes the trained surrogate model on new input data.

        :param inValue: An array or list of values with the same length of the list of input columns (inputCols)
        :return: An array of values with the same length of the list of output columns (outputCols)
        '''

        # Ensure we already have trained regressor before trying to sim
        if self.regressor is not None and len(inValue) == len(self.inputCols):
            out = self.regressor.predict(inValue)
            return out
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