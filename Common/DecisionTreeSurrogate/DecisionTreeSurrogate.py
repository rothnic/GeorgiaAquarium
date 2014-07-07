__author__ = 'Nick'

import numpy as np
import pandas as pd
import neurolab as nl
from scipy import stats
from sklearn.cross_validation import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import gaussian_process
from sklearn.ensemble.partial_dependence import plot_partial_dependence
import cPickle as pickle

class DecisionTreeSurrogate:
    def __init__(self, trainingFile, inputCols, outputCols, regressorFile=None):

        self.inputCols = inputCols
        self.outputCols = outputCols
        self.trainData = pd.read_csv(trainingFile)
        self.regressor = None
        self.inputData = None
        self.outputData = None

        # Load regressor if we have a saved regressor file
        if regressorFile is not None:
            self.regressor = pickle.loads(regressorFile)

    def test(self):
        if self.regressor is not None:
            out = self.regressor.predict(self.inputData)
            scores = cross_val_score(self.regressor, self.inputData, self.outputData, cv=20, scoring='r2')
            print "Cross Validation for Trained Model"
            print "Mean: " + str(scores.mean())
            print "Std: " + str(scores.std()*2)
            print ""
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
        # Select only input columns from pandas dataframe as numpy array
        self.inputData = self.trainData[self.inputCols].values
        self.outputData = self.trainData[self.outputCols].values
        # Create decision tree regressor object
        #self.regressor = DecisionTreeRegressor(random_state=0, max_features=1.0, min_samples_split=2, max_depth=7)
        self.regressor = RandomForestRegressor(n_estimators=n_estimators, n_jobs=-1)
        #scores = cross_val_score(self.regressor, self.inputData, self.outputData, cv=10)

        # Fit regressor to inputs/outputs
        self.regressor.fit(self.inputData, self.outputData)

    def predict(self, inValue):
        # Ensure we already have trained regressorwork before trying to sim
        if self.regressor is not None and len(inValue) == len(self.inputCols):
            out = self.regressor.predict(inValue)
            return out
        else:
            raise Exception

    def print_sim(self, inValues):
        for value in inValues:
            print "Input: " + str(value) + " Output: " + str(self.predict(value))